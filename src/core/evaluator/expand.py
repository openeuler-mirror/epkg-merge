# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import re
from src.core.common import is_pycode
from src.core.constant.tokens import NOT_EXIST

def expand_macro(str_macro, fspath):
    from src.core.config_space import config_space
    str_macro += " "
    patterns = [r'(%%%?{?(.+?)[}" "\s])', '(\${{([-.\(\)\[\]\\\'\\"\w]+)}})']
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
        if k.startswith("${{") and k.endswith("}}"):
            if k.startswith("${{rpmrc."):
                v = v.replace("rpmrc.", "rpmGlobal.")
            elif k.startswith("${{pkg.") or k.startswith("${{pkg["):
                if re.fullmatch("\$\{\{pkg\.has\([-\'\"\w.]+\)}}", k):
                    find_keywords = re.findall("\$\{\{pkg\.has\([-\'\"\w.]+\)}}", k)[0]
                    keywords = find_keywords[1]
                    if re.fullmatch("[\"\'].+[\"\']", keywords):
                        keywords = keywords[1:-1]
                        v = f"pkg.{keywords}" in config_space
                elif re.fullmatch("\$\{\{pkg\.get\([-\'\"\w.]+\)}}", k):
                    find_keywords = re.findall("\$\{\{pkg\.get\([-\'\"\w.]+\)}}", k)[0]
                    keywords = find_keywords[1]
                    if re.fullmatch("[\"\'].+[\"\']", keywords):
                        keywords = keywords[1:-1]
                        v = f"{cspath}.{keywords}"
                elif re.fullmatch("\$\{\{pkg\[[-\'\"\w.]+]}}", k):
                    find_keywords = re.findall("\$\{\{pkg\[[-\'\"\w.]+]}}", k)[0]
                    keywords = find_keywords[1]
                    if re.fullmatch("[\"\'].+[\"\']", keywords):
                        keywords = keywords[1:-1]
                        v = f"{cspath}.{keywords}"
                else:
                    v = v.replace("pkg.", f"{cspath}.")
            else:
                v = f"{cspath}.{v}"
        sub_values[k] = config_space.get_key(v)

        # defineFlags只需要看 是否真的能够获取到值，如果获取到说明是存在的
        if ("defineFlags.+" in k) or ("defineFlags.-" in k):
            if sub_values[k] == NOT_EXIST:
                sub_values[k] = False
            else:
                sub_values[k] = True
    return substitute(str_macro, sub_values)


def substitute(str_macro, sub_values):
    # 先替换长度大的字符串
    # 防止出现%%abcd被%%a先错误替换的情况
    sorted_sub_values = sorted(sub_values.items(), key=lambda x: len(x[0]), reverse=True)
    for sub_value in sorted_sub_values:
        str_macro = str_macro.replace(sub_value[0], str(sub_value[1]))
    return str_macro
