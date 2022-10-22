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
        return 1
    if not right_in:
        return -1

    left_index = type_list.index(left)
    right_index = type_list.index(right)

    if left_index < right_index:
        return 1
    else:
        return -1


def merge_policy_first(collect_str, new_val, merge_params):
    return new_val, False


def merge_policy_concat(collect_str, new_val, merge_params="\n"):
    if collect_str == "":
        return new_val, True
    concat_val = merge_params.join([collect_str, new_val])
    return concat_val, True


def merge_policy_config_concat(collect_str, new_val, merge_params=" \\\n"):
    if collect_str == "":
        return new_val.replace("\n", merge_params), True
    new_val = new_val.replace("\n", merge_params)
    concat_val = merge_params.join([collect_str, new_val])
    return concat_val, True


def merge_policy_pre_concat(collect_str, new_val, merge_params="\n"):
    if collect_str == "":
        return new_val, True
    concat_val = merge_params.join([new_val, collect_str])
    return concat_val, True


def merge_policy_pre_extend(collect_str, new_val, merge_params):
    extend_val = []
    if collect_str == "":
        return new_val, True
    extend_val.extend(new_val)
    extend_val.extend(collect_str)
    return extend_val, True


def merge_policy_extend(collect_str, new_val, merge_params):
    if collect_str == "":
        collect_str = []
    collect_str.extend(new_val)
    return collect_str, True


def merge_policy_append(collect_set, new_val, merge_params):
    return new_val, False


def merge_policy_and(collect_bool, new_val, merge_params):
    return new_val, False


def merge_policy_or(collect_bool, new_val, merge_params):
    return new_val, False


merge_funcs = {
    "merge_policy_concat": merge_policy_concat,
    "merge_policy_append": merge_policy_append,
    "merge_policy_extend": merge_policy_extend,
    "merge_policy_pre_extend": merge_policy_pre_extend,
    "merge_policy_and": merge_policy_and,
    "merge_policy_or": merge_policy_or,
    "merge_policy_first": merge_policy_first,
    "merge_policy_pre_concat": merge_policy_pre_concat,
    "merge_policy_config_concat": merge_policy_config_concat,
}


def get_merge_func(key):
    # 根据类型获取merge_func
    from src.core.config_space import config_space
    from src.core.evaluator.lib.types import get_func

    merge_func, merge_params = get_func(key, "mergeFunc", "mergeParams")
    if merge_func:
        return merge_funcs.get(merge_func), merge_params
    return merge_policy_first, ""
