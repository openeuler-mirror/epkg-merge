# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.


def is_pycode(val: str):
    val = val.strip()
    if not val.startswith("{{"):
        return False
    if not val.endswith("}}"):
        return False
    return True


def eval_python(val: str):
    from src.core.interpreter.interpreter import call
    # result = {
    #     # 代码
    #     'code': py_code,
    #     # 合法性校验
    #     'legality': validate_code(py_code),
    #     # 代码执行
    #     'result': exec_code(py_code)
    # }
    val = val.strip()
    val = val.lstrip("{{")
    val = val.rstrip("}}")
    result = call(val.strip())

    if result["legality"]:
        return result.get("result")
    else:
        raise Exception("pycode parse failed, {}".format(val))
