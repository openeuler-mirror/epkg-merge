# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

def get_func(key, func_name):
    from src.core.config_space import config_space
    temp_key = key
    while temp_key:
        last_temp_key = temp_key.rsplit(".", 1)[0]
        key_refer_attrs = config_space.get_key(f"{temp_key}:referAttrs")
        if key_refer_attrs:
            func_name = config_space.get_key(f"{temp_key}:{func_name}")
            if func_name:
                return func_name

        if last_temp_key == temp_key:
            return None
        temp_key = last_temp_key

