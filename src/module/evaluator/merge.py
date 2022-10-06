# Copyright (c) 2022 Huawei Technologies Co.,Ltd. All rights reserved.
#
# StratoVirt is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan
# PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http:#license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
from src.module.evaluator.lib.merge_funcs import get_merge_func


def merge_sorted(values):
    return values


def merge_overrides(key, values):
    from src.module.config_space import config_space
    temp_values = values
    prepend_values = config_space.get(f"{key}:prepend:values")
    append_values = config_space.get(f"{key}:append:values")
    remove_values = config_space.get(f"{key}:remove:values")
    replace_values = config_space.get(f"{key}:replace:values")
    # 依次处理，这里假设prepend和append是解耦的
    return temp_values


def merge_values(key):
    from src.module.config_space import config_space
    values = config_space.get(f"{key}:values")
    values_sorted = merge_sorted(values)
    values_all = merge_overrides(key, values_sorted)
    merge_func = get_merge_func(key)
    return merge_func(values_all)
