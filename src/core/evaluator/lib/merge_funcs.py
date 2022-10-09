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


def merge_policy_concat(collect_str, new_val):
    pass


def merge_policy_append(collect_set, new_item):
    pass


def merge_policy_and(collect_bool, new_val):
    pass


def merge_policy_or(collect_bool, new_val):
    pass


merge_funcs = {
    "merge_policy_concat": merge_policy_concat,
    "merge_policy_append": merge_policy_append,
    "merge_policy_and": merge_policy_and,
    "merge_policy_or": merge_policy_or,
}


def get_merge_func(key):
    # 	pkgs.bash.phase.build:type <not found>
    # 	pkgs.bash.phase.build:referAttrs <not found>
    # 	pkgs.bash.phase:referAttrs = types.package.phase <found, redirect>
    # 	types.package.phase:type = str <found, finish>
    #
    # 	pkgs.bash.version:checkFunc <not found>
    # 	pkgs.bash.version:referAttrs <not found>
    # 	pkgs.bash:referAttrs = types.package <found, redirect>
    # 	types.package.version:checkFunc = is_version <found, finish>

    # 根据类型获取merge_func
    from src.core.config_space import config_space
    from src.core.evaluator.lib.types import get_func
    merge_func = config_space.get_key(f"{key}:mergeFunc")
    if merge_func:
        return merge_funcs.get(merge_func)
    merge_func = get_func(key, "mergeFunc")
    if merge_func:
        return merge_funcs.get(merge_func)
    return None
