# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import re
from src.core.common import is_pycode

def expand_macro(str_macro, fspath):
    from src.core.config_space import config_space
    str_macro += " "
    patterns = [r'(%%%?{?(.+?)[}" "\s])']
    if is_pycode(str_macro):
        patterns.append(r'(dd?\.(.+?)[" "\s])')
    macro_keys = {}
    cspath = config_space.get_key(f"files.\"{fspath}\".cspath")
    for pattern in patterns:
        for match in re.findall(pattern, str_macro):
            macro_keys[match[0].strip()] = match[1]
    str_macro = str_macro[0:-1]
    sub_values = {}
    for k, v in macro_keys.items():
        if not k.startswith("%%%") and k.startswith("%%"):
            v = f"{cspath}.{v}"
        if not k.startswith("dd") and k.startswith("d"):
            v = f"{cspath}.{v}"
        sub_values[k] = config_space.get_key(v)
    return substitute(str_macro, sub_values)


def substitute(str_macro, sub_values):
    # 先替换长度大的字符串
    # 防止出现%%abcd被%%a先错误替换的情况
    sorted_sub_values = sorted(sub_values.items(), key=lambda x: len(x[0]), reverse=True)
    for sub_value in sorted_sub_values:
        str_macro = str_macro.replace(sub_value[0], str(sub_value[1]))
    return str_macro
