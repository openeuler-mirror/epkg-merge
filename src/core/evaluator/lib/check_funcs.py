# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import re
import os

# str
def is_str(key, value, check_func, check_params):
    if not isinstance(value, str):
        err_code = {
            'value': value,
            'err_msg': 'Offered value is not in type str!'
            }
        return err_code

    return None

def is_one_of(key, value, check_func, check_params):
    available_values = check_params
    if not available_values:
        err_code = {
            'value': value,
            'err_msg': 'Get no checkParams for checkFunc: is_oneof!'
            }
        return err_code

    available_values = available_values.split(',')
    if not value in available_values:
        err_code = {
            'value': value,
            'available_values': available_values,
            'err_msg': 'Offered value is not an available value!'
            }
        return err_code

    return None

def is_some_of(key, value, check_func, check_params):
    available_values = check_params
    if not available_values:
        err_code = {
            'value': value,
            'err_msg': 'Get no checkParams for checkFunc: is_oneof!'
            }
        return err_code

    sub_values = value.split(',')
    available_values = available_values.split(',')
    if not set(sub_values) <= set(available_values):
        err_code = {
            'value': value,
            'available_values': available_values,
            'err_msg': 'Offered values are not all in available values!'
            }
        return err_code

    return None

def is_pattern(key, value, check_func, check_params):
    pattern = check_params
    if not pattern:
        err_code = {
            'value': value,
            'err_msg': 'Get no checkParams for checkFunc: pattern!'
            }
        return err_code

    if not re.match(r'{}'.format(pattern), value):
        err_code = {
            'value': value,
            'available_values': pattern,
            'err_msg': 'Offered value is not in right pattern!'
            }
        return err_code

    return None

def is_package(key, value, check_func, check_params):
    pass # check value is a package name?

def is_path(key, value, check_func, check_params):
    if os.path.exists(value):
        return None
    else:
        err_code = {
            'value': value,
            'err_msg': 'Offered path is not exists!'
            }
        return err_code

def is_env_path(key, value, check_func, check_params):
    env_path = check_params
    if not env_path:
        err_code = {
            'value': value,
            'err_msg': 'Get no checkParams for checkFunc: is_PATH!'
            }
        return err_code

    if not value in env_path.split(":"):
        err_code = {
            'value': value,
            'env_path': env_path,
            'err_msg': 'Offered path is not in the env PATH!'
            }
        return err_code

    return None

def is_version(key, value, check_func, check_params):
    # version string should like: 1.1, 1.1.1
    # it should startwith and end with a integer, and filled with ingeter and '.' between them.
    if re.match("^[0-9][0-9.]*[0-9]$", str(value)):
        return None

    err_code = {
        'value': value,
        'err_msg': 'Offered value is not in right version format.'
        }
    return err_code

def is_release(key, value, check_func, check_params):
    pass # check value is in release format?

# int
def is_int(key, value, check_func, check_params):
    if not isinstance(value, int):
        err_code = {
            'value': value,
            'err_msg': 'Offered value is not an integer!'
            }
        return err_code

    return None

def is_between(key, value, check_func, check_params):
    key_limits = check_params
    if not key_limits:
        err_code = {
            'value': value,
            'err_msg': 'Get no checkParams for checkFunc: is_between!'
            }
        return err_code

    if not isinstance(value, int):
        err_code = {
            'value': value,
            'err_msg': 'Offered value is not a integer!'
            }
        return err_code

    min_v, max_v = key_limits.split(',')
    if not (int(value) >= int(min_v) and int(value) <= int(max_v)):
        err_code = {
            'value': value,
            'value_limits': key_limits,
            'err_msg': 'Offered value is beyond the value limits!'
            }
        return err_code

    return None

# float
def is_float(key, value, check_func, check_params):
    if not isinstance(value, float):
        err_code = {
            'value': value,
            'err_msg': 'Offered value is not a float!'
            }
        return err_code
    return None

# bool
def is_bool(key, value, check_func, check_params):
    if isinstance(value, bool):
        return None
    else:
        err_code = {
            'value': value,
            'err_msg': 'Offered value is not in type: bool!'
            }
        return err_code

def is_list(key, value, check_func, check_params):
    if not isinstance(value, list):
        err_code = {
            'value': value,
            'err_msg': 'Offered value is not a list!'
            }
        return err_code
    return None

def is_str_list(key, value, check_func, check_params):
    if not isinstance(value, list):
        err_code = {
            'value': value,
            'err_msg': 'Offered value is not a list!'
            }
        return err_code

    for s in value:
        if isinstance(s, str):
            continue
        else:
            err_code = {
                'value': value,
                'value_ele': s,
                'err_msg': 'Offered value contains non-string elementas!'
                }
            return err_code
    return None

# strSet
def is_str_set(key, value, check_func, check_params):
    str_set = check_params
    value_list = value.split(',')
    str_set_list = str_set.split(',')

    setted_value_list =  sorted(list(set(value_list)), key = value_list.index)

    if not setted_value_list == value_list:
        err_code = {
            'value': value,
            'err_msg': 'Offered value is duplicated!'
            }
        return err_code
    
    if not setted_value_list == sorted(value_list, key = str_set_list.index):
        err_code = {
            'value': value,
            'err_msg': 'Offered value is not in the required order!'
            }
        return err_code

    return None

def no_check_func(key, value, check_params):
    return None

check_funcs = {
	"is_str": is_str,
        "is_oneof": is_one_of,
        "is_someof": is_some_of,
        "is_pattern": is_pattern,
        "is_package": is_package,
        "is_path": is_path,
        "is_PATH": is_env_path,
        "is_version": is_version,
        "is_release": is_release,
        "is_int": is_int,
        "is_between": is_between,
        "is_float": is_float,
        "is_bool": is_bool,
        "is_list": is_list,
        "is_strList": is_str_list,
        "is_strSet": is_str_set,
        "no_check_func": no_check_func
}

def value_check_func(key, value, check_func, check_params):
    if not check_funcs.get(check_func):
        check_func = 'no_check_func'
    return check_funcs.get(check_func)(key, value, check_func, check_params)
