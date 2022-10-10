# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.


def sort_doctype(left, right):
    type_list = ["base", "sw-package", "hw-chip", "hw-board", "hw-machine",
                 "distro", "build", "env-system", "env-project", "env-user"]
    if left == right:
        return 0
    left_in = left in type_list
    right_in = right in type_list

    if (not left_in) and (not right_in):
        return 0
    if not left_in:
        return -1
    if not right_in:
        return 1

    left_index = type_list.index(left)
    right_index = type_list.index(right)

    if left_index < right_index:
        return -1
    else:
        return 1


def merge_policy_first(collect_str, new_val, merge_params):
    return new_val, False


def merge_policy_concat(collect_str, new_val, merge_params):
    return new_val, False


def merge_policy_append(collect_set, new_val, merge_params):
    return new_val, False


def merge_policy_and(collect_bool, new_val, merge_params):
    return new_val, False


def merge_policy_or(collect_bool, new_val, merge_params):
    return new_val, False


merge_funcs = {
    "merge_policy_concat": merge_policy_concat,
    "merge_policy_append": merge_policy_append,
    "merge_policy_and": merge_policy_and,
    "merge_policy_or": merge_policy_or,
    "merge_policy_first": merge_policy_first,
}


def get_merge_func(key):
    # 根据类型获取merge_func
    from src.core.config_space import config_space
    from src.core.evaluator.lib.types import get_func
    merge_func = config_space.get_key(f"{key}:mergeFunc")
    if merge_func:
        return merge_funcs.get(merge_func), config_space.get(f"{key}:mergeParams", "")
    merge_func, merge_params = get_func(key, "mergeFunc", "mergeParams")
    if merge_func:
        return merge_funcs.get(merge_func), merge_params
    return merge_policy_first, ""
