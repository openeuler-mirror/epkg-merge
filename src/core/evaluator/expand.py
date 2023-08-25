# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import re
import yaml
from distutils.version import LooseVersion
from src.core.common import is_pycode
from src.core.constant.tokens import NOT_EXIST
from src.core.loader.lib.enums import ImportConfig

def expand_macro(str_macro, fspath):
    from src.core.config_space import config_space
    str_macro += " "
    # patterns = [r'(%%%?{?(.+?)[}" "\s])', '(\${{([-.\(\)\[\]\\\'\\"\w]+)}})']
    patterns = [r'(%%%?{?(.+?)[}" "\s])', r'(@([.\d]*:?[.\d]*))', '(\${{([-.\(\)\[\]\\\'\\"\w]+)}})']
    if is_pycode(str_macro):
        patterns.append(r'(dd?\.(.+?)[" "\s])')
    macro_keys = {}
    cspath = config_space.get_key(f"files.\"{fspath}\".cspath")
    for p_index, pattern in enumerate(patterns):
        if p_index == 1 and " when " not in str_macro:
            continue
        for match in re.findall(pattern, str_macro):
            macro_keys[match[0].strip()] = match[1]
    str_macro = str_macro[0:-1]
    sub_values = {}
    for k, v in macro_keys.items():
        # if not k.startswith("%%%") and k.startswith("%%"):
        #     v = f"{cspath}.{v}"
        if k.startswith("@") and re.search("\d", v):
            if ":" not in v:
                v = f"version=={v}"
            elif v.startswith(":"):
                v = f"version<={v.lstrip(':')}"
            elif v.endswith(":"):
                v = f"version>={v.rstrip(':')}"
            else:
                v = v.replace(":", "<=version<=")
        if not k.startswith("dd") and k.startswith("d"):
            v = f"{cspath}.{v}"
        if k.startswith("${{") and k.endswith("}}"):
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
            elif k.startswith("${{top["):
                find_keywords = re.findall(ImportConfig.TOP_KEY.value, k)[0]
                keywords = find_keywords[1]
                if "." not in keywords:
                    raise Exception("error format in %s" % k)
                v = f"top.{keywords}"
                if v not in config_space:
                    load_top_yaml_info(fspath, cspath, keywords.split(".")[1])
            else:
                v = f"{cspath}.{v}"
        if isinstance(v, bool):
            sub_values[k] = str(v).lower()
        else:
            sub_values[k] = config_space.get_key(v)

        # defineFlags只需要看 是否真的能够获取到值，如果获取到说明是存在的
        if ("defineFlags.+" in k) or ("defineFlags.-" in k):
            if sub_values[k] == NOT_EXIST:
                sub_values[k] = False
            else:
                sub_values[k] = True
        elif k.startswith("@") and "version" in v:
            sub_values[k] = parse_version_expression(v, cspath)
    return substitute(str_macro, sub_values)


def substitute(str_macro, sub_values):
    # 先替换长度大的字符串
    # 防止出现%%abcd被%%a先错误替换的情况
    sorted_sub_values = sorted(sub_values.items(), key=lambda x: len(x[0]), reverse=True)
    for sub_value in sorted_sub_values:
        str_macro = str_macro.replace(sub_value[0], str(sub_value[1]))
    return str_macro


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


def parse_version_expression(expression, cspath):
    from src.core.config_space import config_space
    version = config_space.get(f"{cspath}.version")
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
