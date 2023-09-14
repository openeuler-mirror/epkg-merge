# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import re

from distutils.version import LooseVersion
from src.log import log
import core


def version_compare():
    pass


def parse_version_expression(expression, cspath):
    from src.core.config_space import config_space
    version = config_space.get_key(f"{cspath}.version")
    if version is None:
        return False
    while True:
        if re.fullmatch("%\{?\W?(\w+)}?", version):
            base_param = re.findall("%\{?\W?(\w+)}?", version)[0]
            version = config_space.get(f"{cspath}.rpmGlobal.{base_param}")
        elif re.fullmatch("$\{\{rpmGlobal\.(\s+)}}", version):
            base_param = re.findall("$\{\{rpmGlobal\.(\s+)}}", version)[0]
            version = config_space.get(f"{cspath}.rpmGlobal.{base_param}")
        else:
            break
    if "==" in expression:
        target_version = expression.split("==")[1]
        return version == target_version
    elif ">=" in expression:
        target_version = LooseVersion(expression.split(">=")[1])
        return LooseVersion(version) >= target_version
    elif expression.startswith("version<="):
        target_version = LooseVersion(expression.split("<=")[1])
        return LooseVersion(version) <= target_version
    else:
        least_version, _, largest_version = expression.split("<=")
        return LooseVersion(least_version) <= LooseVersion(version) <= LooseVersion(largest_version)


def eval_python(val: str):
    import src.core.interpreter.executor
    # result = {
    #     # 代码
    #     'code': py_code,
    #     # 合法性校验
    #     'legality': validate_code(py_code),
    #     # 代码执行
    #     'result': exec_code(py_code)
    # }
    val = val.strip()
    result = src.core.interpreter.executor.call(val.strip())

    if result["legality"]:
        return result.get("result")
    else:
        log.debug("pycode parse failed, {}".format(val))
        return val
