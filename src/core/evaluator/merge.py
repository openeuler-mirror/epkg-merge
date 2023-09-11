# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
from src.core.evaluator.lib.merge_funcs import get_merge_func
from functools import cmp_to_key
from src.core.evaluator.expand import expand_macro
from src.core.common import is_pycode, eval_python
from src.core.evaluator.lib.merge_funcs import sort_doctype
from src.log import log
from src.core.evaluator.parser.when_parser import parser
from src.core.constant.tokens import NOT_EXIST


def cmp(v_left, v_right):
    from src.core.config_space import config_space
    # 如何获取value的
    v_left_fspath = v_left["fspath"]
    v_right_fspath = v_right["fspath"]
    v_left_doctype = config_space.get_key(f"files.\"{v_left_fspath}\".docType")
    v_right_doctype = config_space.get_key(f"files.\"{v_right_fspath}\".docType")
    sort_result = sort_doctype(v_left_doctype, v_right_doctype)
    if sort_result != 0:
        return sort_result

    v_left_layername = config_space.get_key(f"files.\"{v_left_fspath}\".cspath")
    v_right_layername = config_space.get_key(f"files.\"{v_right_fspath}\".cspath")
    if v_left_layername < v_right_layername:
        return 1
    elif v_left_layername == v_right_layername:
        return 0
    else:
        return -1


def eval_val(val):
    result = val
    if is_pycode(val):
        result = eval_python(val)
    return result


def is_when(item):
    fspath = item.get('fspath')
    when_statement = ""
    try:
        when_statement = item.get("when")
        when_value = get_val(when_statement, fspath)
    except Exception as _:
        log.error(f"expand {item.get('when')} failed!")
        when_value = False

    if when_value == NOT_EXIST:
        return False

    if when_statement:
        when_result = parser.parse(when_value)
        if not when_result or str(when_result).upper() == "FALSE":
            return False

    return True


def replace_item(ori_value, items: list) -> object:
    ori_type = type(ori_value)
    if ori_type is list:
        result_values = []
    else:
        result_values = ori_value

    for i in items:
        if not is_when(i):
            continue
        item_value = i.get("value")
        item_type = type(item_value)
        if item_type == ori_type:
            result_values = item_value
        elif item_type is str and ori_type is list:
            result_values = [item_type]

    return result_values


def remove_cal(ori_value, sub_value) -> object:
    result_values = []
    ori_type = type(ori_value)
    if ori_type is list:
        for sub_ori_value in ori_value:
            if sub_value in sub_ori_value and " " in sub_ori_value:
                new_sub_value = sub_ori_value.split(" ").remove(sub_value).join(" ")
                if new_sub_value:
                    result_values.append(new_sub_value)
            elif sub_value != sub_ori_value:
                result_values.append(sub_ori_value)
    elif ori_type is str:
        if sub_value in ori_value and " " in ori_value:
            new_sub_value = ori_value.split(" ").remove(sub_value).join(" ")
            if new_sub_value:
                result_values.append(new_sub_value)
        elif sub_value != ori_value:
            result_values.append(ori_value)
        result_values = result_values[0]

    return result_values


def remove_item(ori_value, items: list) -> object:
    ori_type = type(ori_value)
    result_values = ori_value

    for i in items:
        if not is_when(i):
            continue
        item_value = i.get("value")
        item_type = type(item_value)
        if item_type is list:
            for sub_values in item_value:
                for sub_value in sub_values.split(" "):
                    result_values = remove_cal(result_values, sub_value)

        elif item_type is str:
            for sub_value in item_value.split(" "):
                result_values = remove_cal(result_values, sub_value)

    return result_values


def merge_sorted(values):
    # 如何通过fspath 获取doctype
    values_sorted = sorted(values, key=cmp_to_key(cmp))
    return values_sorted


def merge_overrides(key, values):
    from src.core.config_space import config_space
    temp_values = values
    remove_values = config_space.get(f"{key}:remove:values", [])
    replace_values = config_space.get(f"{key}:replace:values", [])
    if not (remove_values or replace_values):
        return values

    if replace_values:
        temp_values = replace_item(temp_values, replace_values)

    if remove_values:
        temp_values = remove_item(temp_values, remove_values)

    return temp_values


def convert_val(val, fspath):
    if type(val) is not str:
        return val
    val_expanded = expand_macro(val, fspath)
    value = eval_val(val_expanded)
    return value


def get_val(val, fspath):
    if val is None:
        return None
    if type(val) is not list:
        return convert_val(val, fspath)
    temp_val = []
    for i, value in enumerate(val):
        val_real = convert_val(value, fspath)
        temp_val.append(val_real)
    return temp_val


def merge_with_func(merge_func, merge_params, values_all):
    current = ""

    if not values_all:
        return NOT_EXIST

    for cur_value in values_all:
        raw_value = cur_value.get("value", "")
        value = get_val(raw_value, cur_value.get('fspath'))
        current, is_continue = merge_func(current, value, merge_params)
        if not is_continue:
            break

    return current


def merge_values(key):
    from src.core.config_space import config_space
    values = config_space.get(f"{key}:values")
    values_sorted = merge_sorted(values)
    values_all = values_sorted
    values_all = list(filter(is_when, values_all))
    merge_func, merge_params = get_merge_func(key)
    final_value = merge_with_func(merge_func, merge_params, values_all)
    final_value = merge_overrides(key, final_value)
    return final_value
