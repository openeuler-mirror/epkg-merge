# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import re
from typing import overload, Any, Dict
from src.core.constant.tokens import IF_TOKEN


def expand_implicit_fields(val: Any, implicit_fields: Dict[str, str] = None) -> str:
    if implicit_fields and isinstance(val, str):
        for k, v in implicit_fields.items():
            val = str(val).replace(k, v)
    return val


def merge_key(key: str, prefix: str) -> (str, str):
    if IF_TOKEN not in prefix:
        return key, prefix
    prefix_key, if_statement = prefix.split(IF_TOKEN)
    key = str(key)
    if IF_TOKEN in key:
        new_key = key + " && {}".format(if_statement)
    else:
        new_key = key + " when {}".format(if_statement)
    new_key = new_key.strip()
    prefix_key = prefix_key.strip()
    return new_key, prefix_key


def expand_key(key: Any, prefix: str = None) -> str:
    if not prefix:
        return key
    key, prefix = merge_key(key, prefix)
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
        if prefix is not None and re.fullmatch("pkgs\.\w+\.defineFlags\.[\w-]+", prefix):
            if "when" in val:
                prefix += " when {0}".format(val.get("when"))
                del val["when"]
            return {
                expand_implicit_fields(prefix, implicit_fields): val
            }
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
