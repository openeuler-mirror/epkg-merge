# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import re
import yaml
from distutils.version import LooseVersion

from src.core.constant.tokens import NOT_EXIST
from src.core.loader.lib.enums import ImportConfig
from src.core.lib.utils import eval_python, parse_version_expression


def get_version_value(v, cspath):
    if ":" not in v:
        v = f"version=={v}"
    elif v.startswith(":"):
        v = f"version<={v.lstrip(':')}"
    elif v.endswith(":"):
        v = f"version>={v.rstrip(':')}"
    else:
        v = v.replace(":", "<=version<=")
    return parse_version_expression(v, cspath)


def get_macro_values(v, cspath):
    from src.core.config_space import config_space
    # ${{ xxx  }} 其中xxx 可能是多个语句，需要隔离并提取其中top和pkg部分
    # 先替换top, 在替换pkg
    rc_match = re.findall(ImportConfig.RC_VAL.value, v)
    for temp_match in rc_match:
        cspath_pkg_key = temp_match.replace("rpmrc.", "rpmGlobal.", 1)
        v = v.replace(temp_match, config_space.get_key(cspath_pkg_key))

    rc_match = re.findall(ImportConfig.RG_VAL.value, v)
    for temp_match in rc_match:
        cspath_pkg_key = temp_match
        v = v.replace(temp_match, config_space.get_key(cspath_pkg_key))

    top_match = re.findall(ImportConfig.TOP_VAL.value, v)
    for temp_match in top_match:
        cspath_pkg_key = temp_match.replace("top.", "", 1)
        v = v.replace(temp_match, config_space.get_key(cspath_pkg_key))
    pkg_match = re.findall(ImportConfig.PKG_VAL.value, v)
    for temp_match in pkg_match:
        cspath_pkg_key = temp_match.replace("pkg.", cspath + ".", 1)
        key_value = config_space.get_key(cspath_pkg_key)
        if ".defineFlags." in cspath_pkg_key:
            if key_value == NOT_EXIST:
                key_value = "False"
            else:
                key_value = "True"

        v = v.replace(temp_match, str(key_value))
    return v


def substitute(str_macro, sub_values):
    # 先替换长度大的字符串
    # 防止出现%%abcd被%%a先错误替换的情况
    sorted_sub_values = sorted(sub_values.items(), key=lambda x: len(x[0]), reverse=True)
    for sub_value in sorted_sub_values:
        str_macro = str_macro.replace(sub_value[0], str(sub_value[1]))
    return str_macro


def expand_macro(str_macro, fspath, is_when_statement=False):
    from src.core.config_space import config_space
    str_macro += " "
    macro_keys = {}
    sub_values = {}
    cspath = config_space.get_key(f"files.\"{fspath}\".cspath")

    patterns = [r'(\${{(.+?)}})']
    if is_when_statement:
        patterns.append(r'(@([-+.\d]*:?[-+.\d]*))')

    for p_index, pattern in enumerate(patterns):
        for match in re.findall(pattern, str_macro):
            if p_index == 1 and not re.search("\d", match[1]):
                continue
            macro_keys[match[0].strip()] = match[1]
    str_macro = str_macro[0:-1]

    for k, v in macro_keys.items():
        if k.startswith("@") and re.search("\d", v):
            v = get_version_value(v, cspath)
            # sub_values[k] = v
        if k.startswith("${{") and k.endswith("}}"):
            v = get_macro_values(v, cspath)
            try:
                float(v)
            except ValueError:
                v = eval_python(v)
            # sub_values[k] = v

        sub_values[k] = str(v)

    return substitute(str_macro, sub_values)


def load_top_yaml_info(fspath, cspath, package):
    from src.core.config_space import config_space
    package_fspath = fspath.replace(cspath.split(".")[-1], package)
    with open(package_fspath, encoding="utf-8") as f1:
        configs = yaml.safe_load(f1)
        package_content = f1.read()
    import_words = re.findall(ImportConfig.TOP_KEY.value, package_content)
    for import_word in import_words:
        pkg_cspath = import_word[1]
        if "." in pkg_cspath:
            raise Exception("Can't load full package")
        package_name = pkg_cspath.split(".")[0]
        load_top_yaml_info(package_fspath, pkg_cspath, package_name)
    for k, v in configs.items():
        config_space.add_key(f"top.pkgs.{package}.{k}", v, package_fspath)


def _old_parse():
    from src.core.config_space import config_space
    k = ""
    v = ""
    cspath = ""
    fspath = ""
    if k.startswith("${{rpmrc."):
        v = v.replace("rpmrc.", "rpmGlobal.")
    elif k.startswith("${{pkg.") or k.startswith("${{pkg["):
        if re.fullmatch(ImportConfig.PKG_HAS.value, k):
            find_keywords = re.findall(ImportConfig.PKG_HAS.value, k)[0]
            keywords = find_keywords[1]
            if re.fullmatch("[\"\'].+[\"\']", keywords):
                keywords = keywords[1:-1]
            v = f"pkg.{keywords}" in config_space
        elif re.fullmatch(ImportConfig.PKG_GET.value, k):
            find_keywords = re.findall(ImportConfig.PKG_GET.value, k)[0]
            keywords = find_keywords[1]
            if re.fullmatch("[\"\'].+[\"\']", keywords):
                keywords = keywords[1:-1]
            v = f"{cspath}.{keywords}"
        elif re.fullmatch(ImportConfig.PKG_KEY.value, k):
            find_keywords = re.findall(ImportConfig.PKG_KEY.value, k)[0]
            keywords = find_keywords[1]
            if re.fullmatch("[\"\'].+[\"\']", keywords):
                keywords = keywords[1:-1]
            v = f"{cspath}.{keywords}"
        else:
            v = v.replace("pkg.", f"{cspath}.")
    elif k.startswith("${{top[") or k.startswith("${{top."):
        if re.fullmatch(ImportConfig.TOP_KEY.value, k):
            find_keywords = re.findall(ImportConfig.TOP_KEY.value, k)[0]
            keywords = find_keywords[1]
            if "." not in keywords:
                raise Exception("error format in %s" % k)
            v = f"top.{keywords}"
            if v not in config_space:
                load_top_yaml_info(fspath, cspath, keywords.split(".")[1])
        elif re.fullmatch(ImportConfig.TOP_HAS.value, k):
            find_keywords = re.findall(ImportConfig.TOP_KEY.value, k)[0]
            keywords = find_keywords[1]
            if re.fullmatch("[\"\'].+[\"\']", keywords):
                keywords = keywords[1:-1]
            v = f"top.{keywords}" in config_space
