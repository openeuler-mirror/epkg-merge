# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
from typing import overload, Any, Dict


def expand_implicit_fields(val: Any, implicit_fields: Dict[str, str] = None) -> str:
    if implicit_fields and isinstance(val, str):
        for k, v in implicit_fields.items():
            val = str(val).replace(k, v)
    return val


def expand_key(key: Any, prefix: str = None) -> str:
    if not prefix:
        return key
    if isinstance(key, str) and key.startswith(":"):
        return f"{prefix}{key}"
    return f"{prefix}.{key}"


@overload
def expand_yaml(val: dict, prefix: str = None, implicit_fields: Dict[str, str] = None) -> dict:
    ...


@overload
def expand_yaml(val: list, prefix: str = None, implicit_fields: Dict[str, str] = None) -> dict:
    ...


@overload
def expand_yaml(val, prefix: str = None, implicit_fields: Dict[str, str] = None) -> dict:
    ...


def expand_yaml(val, prefix: str = None, implicit_fields: Dict[str, str] = None) -> dict:
    if isinstance(val, dict):
        result = dict()
        for k, v in val.items():
            key = expand_implicit_fields(expand_key(k, prefix), implicit_fields)
            result.update(expand_yaml(v, key, implicit_fields))
        return result
    elif isinstance(val, list):
        return {
            expand_implicit_fields(prefix, implicit_fields): [expand_implicit_fields(v, implicit_fields) for v in val]
        }
    else:
        return {expand_implicit_fields(prefix, implicit_fields): expand_implicit_fields(val, implicit_fields)}
