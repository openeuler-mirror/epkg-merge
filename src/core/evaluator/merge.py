# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
from src.core.evaluator.lib.merge_funcs import get_merge_func
from functools import cmp_to_key
from src.core.evaluator.expand import expand_macro
from src.core.common import is_pycode
from src.core.py_interpreter.pycode import eval_python
from src.core.evaluator.lib.merge_funcs import sort_doctype


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
    else:
        return -1


def eval_val(val):
    result = val
    if is_pycode(val):
        result = eval_python(val)
    return result


def merge_sorted(values):
    # 如何通过fspath 获取doctype
    values_sorted = sorted(values, key=cmp_to_key(cmp))
    return values_sorted


def merge_overrides(key, values):
    from src.core.config_space import config_space
    temp_values = values
    prepend_values = config_space.get(f"{key}:prepend:values")
    append_values = config_space.get(f"{key}:append:values")
    remove_values = config_space.get(f"{key}:remove:values")
    replace_values = config_space.get(f"{key}:replace:values")
    # 依次处理，这里假设prepend和append是解耦的
    for i in prepend_values:
        if i.info in temp_values:
            temp_values.insert(temp_values.index(i.info), i)

    for i in append_values:
        if i.info in temp_values:
            temp_values.insert(temp_values.index(i.info + 1), i)

    for i in replace_values:
        if i.info in temp_values:
            temp_values[temp_values.index(i.info)] = i

    for i in remove_values:
        if i.info in temp_values:
            temp_values.remove(i)

    return temp_values


def convert_val(val, fspath):
    if type(val) is not str:
        return val
    val_expanded = expand_macro(val, fspath)
    value = eval_val(val_expanded)
    return value


def get_val(val, fspath):
    if val is None:
        return True
    if type(val) is not list:
        return convert_val(val, fspath)
    temp_val = []
    for i, value in enumerate(val):
        val_real = convert_val(value, fspath)
        temp_val.append(val_real)
    return temp_val


def merge_with_func(merge_func, merge_params, values_all):
    current = ""

    for cur_value in values_all:
        fspath = cur_value.get('fspath')
        when_value = get_val(cur_value.get("when"), fspath)
        if not when_value:
            continue
        raw_value = cur_value.get("value", "")
        value = get_val(raw_value, fspath)
        current, is_continue = merge_func(current, value, merge_params)
        if not is_continue:
            break
    return current


def merge_values(key):
    from src.core.config_space import config_space
    values = config_space.get(f"{key}:values")
    values_sorted = merge_sorted(values)
    # values_all = merge_overrides(key, values_sorted)
    values_all = values_sorted
    merge_func, merge_params = get_merge_func(key)
    return merge_with_func(merge_func, merge_params, values_all)
