# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

def get_func(key, func_name, params_name):
    from src.core.config_space import config_space

    merge_func = config_space.get_key(f"{key}:{func_name}")
    if merge_func:
        return merge_func, config_space.get(f"{key}:{params_name}", "")

    temp_key = key
    last_key = key.split(".")[-1]
    while temp_key:
        if temp_key == "pkgs":
            key_refer_attrs = "types.package"
        else:
            key_refer_attrs = config_space.get(f"{temp_key}:referAttrs")
        if key_refer_attrs:
            func_ = config_space.get(f"{key_refer_attrs}.{last_key}:{func_name}")
            if func_:
                return func_, config_space.get(f"{key_refer_attrs}.{last_key}:{params_name}", "")
        last_temp_key = temp_key.rsplit(".", 1)[0]
        if last_temp_key == temp_key:
            return None, ""
        temp_key = last_temp_key

