# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

from src.core.evaluator.lib.check_funcs import value_check_func

def check_value(key, value):
    from src.core.evaluator.lib.types import get_func
    check_func, check_params = get_func(key, "checkFunc", "checkParams")

    if check_func:
        check_func_result = value_check_func(key, value, check_func, check_params)
        if check_func_result:
            print(check_func_result)
            return False
        return True

    err_code = {
        'key': key,
        'value': value,
        'err_msg': 'No checkFunc specified for key: ' + key + '!'
        }
    print(err_code)

    return True
