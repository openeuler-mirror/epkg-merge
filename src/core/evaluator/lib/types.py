# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
from src.core.constant.tokens import NOT_EXIST

def get_referAttrs(pkg_key):
    from src.core.config_space import config_space
    fspaths = config_space.get_key(f"{pkg_key}:fspath")
    for path_item in fspaths:
        refer_attrs = config_space.get(f'files."{path_item}":referAttrs', None)
        if refer_attrs:
            return refer_attrs

    else:
        return None


def gen_keys(key):
    pkg_key = ".".join(key.split(".")[:2])
    key_content = ".".join(key.split(".")[2:])
    pre_keys = [pkg_key]
    refer_attrs = get_referAttrs(pkg_key)
    if refer_attrs is not None:
        pre_keys.append(refer_attrs)

    sub_keys = [key_content]
    if "subpackage." in key_content:
        sub_keys.append(".".join(key_content.split(".")[2:]))

    for key_content_name in sub_keys[:2]:
        if ".source." in key or ".patchset." in key or ".phase." in key:
            sub_keys.append(".".join(key_content_name.split(".")[:-1]))

        if "meta." in key_content_name:
            sub_keys.append(key_content_name.replace("meta.", ""))

    keys = []
    for pre_key in pre_keys:
        for sub_key in sub_keys:
            keys.append(".".join([pre_key, sub_key]))
    return keys


def get_func(key, func_name, params_name):
    from src.core.config_space import config_space

    merge_func = config_space.get_key(f"{key}:{func_name}")
    if merge_func != NOT_EXIST:
        return merge_func, config_space.get(f"{key}:{params_name}", "")

    keys = gen_keys(key)
    for key_item in keys:
        merge_func = config_space.get_key(f"{key_item}:{func_name}")
        if merge_func != NOT_EXIST:
            return merge_func, config_space.get(f"{key_item}:{params_name}", "")
    return None, ""
