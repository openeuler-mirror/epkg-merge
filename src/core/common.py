# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

def is_pycode(val:str):
    val = val.strip()
    if not val.startswith("{{"):
        return False
    if not val.endswith("}}"):
        return False
    return True