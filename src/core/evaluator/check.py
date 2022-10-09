# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
from src.core.evaluator.lib.check_funcs import get_check_func

def check_value(key, value):
    check_func = get_check_func(key)
    return check_func(value)
