# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os.path
import re

import yaml
from src.core.loader.yaml_loader import YamlLoader
from src.core.loader.lib.load_helper import expand_yaml, expand_implicit_fields
from src.core.loader.lib.enums import Directory
from src.core.evaluator.merge import merge_values
from src.core.evaluator.transform import transform_key_default
from src.core.common import format_package_json
from src.core.evaluator.check import check_value
from src.core.constant.tokens import NOT_EXIST
from src.log import log
from src.core.lib.exclude_key import is_strategy_key, is_yaml_key
import platform


def make_synchronized(func):
    import threading
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


def get_key_fspath(key):
    key = key.rsplit(":", 1)[0]
    temp_key = key
    while True:
        raw_key = temp_key
        fspath_list = config_space.get(f"{raw_key}:fspath", None)
        if fspath_list:
            break
        raw_key = temp_key.rsplit(".", 1)[0]
        if temp_key == raw_key:
            break
        temp_key = raw_key
    return raw_key, fspath_list


class InheritConfig:
    def __init__(self):
        self.value = None
        self.fspath = ""
        self.cspath = ""


class ConfigSpace(dict):
    instance = None
    fspath_loaded = []
    checked_failed_keys = []

    @make_synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = dict.__new__(cls, *args, **kwargs)
        return cls.instance

    def get_key_value(self, key):
        value = self.get(key)
        if value is not None:
            return value

        values = self.get(f"{key}:values", NOT_EXIST)
        if values == NOT_EXIST:
            return self.get(f"{key}:default", NOT_EXIST)

        value = merge_values(key)
        if value == NOT_EXIST:
            return NOT_EXIST

        if key in ConfigSpace.checked_failed_keys:
            return None

        if not check_value(key, value):
            ConfigSpace.checked_failed_keys.append(key)
            return None

        self[key] = value
        return value

    def get_key(self, key):
        raw_key, fspath_list = get_key_fspath(key)
        if isinstance(fspath_list, list):
            for fspath in fspath_list:
                # 如果文件不在加载列表中，则添加到加载列表
                if fspath not in ConfigSpace.fspath_loaded:
                    YamlLoader(raw_key, fspath).load()
                    ConfigSpace.fspath_loaded.append(fspath)
        value = self.get_key_value(key)
        return value

    def add_key(self, key, value, fspath):
        key_info = transform_key_default(key, value, fspath)
        for k, v in key_info.items():
            if is_strategy_key(k):
                self[k] = v["value"]
                continue
            self.setdefault(f"{k}:values", []).append(v)
        return list(key_info.keys())

    def get_package(self, package_name):
        pre_name = f"pkgs.{package_name}"
        package_fspath = f"{pre_name}:fspath"
        if package_fspath not in config_space:
            log.error(f"{package_name} not in layers, please check it")
            return {}

        package_info = {}
        self.get_key(pre_name)
        self.load_inherit()
        loaded_keys = config_space.get_key(f"pkgs.{package_name}:loadedKeys")
        for key in loaded_keys:
            value = config_space.get_key(key)
            if re.search("\$\{\{pkg\.\w+}}", key):
                key = expand_implicit_fields(key, {"${{pkg.name}}": package_name})
            if value == NOT_EXIST:
                continue
            if not is_yaml_key(key):
                continue
            short_key = key.replace(f"{pre_name}.", "")
            base_key = key.split(".")[-1]
            if ".defineFlags." in key and isinstance(value, dict):
                if f"{pre_name}.use.{base_key}" in loaded_keys:
                    if "default" in value:
                        value["default"] = config_space.get_key(f"{pre_name}.use.{base_key}")
            package_info[short_key] = value

        return package_info

    def load_inherit(self):
        if "base_layer" not in inherit_config:
            log.error("Can't identify the baseOS, the types may be missing")
            return
        for k, v in inherit_config.items():
            if k == "base_layer":
                self["base_layer"] = v
                continue
            inherit = InheritConfig()
            inherit.value = v.get("value")
            inherit.cspath = v.get("cspath")
            layer_name = v.get("fspath").split("pkgs")[0].split(os.sep)[-2]
            inherit.fspath = v.get("fspath").replace(layer_name, self["base_layer"])
            self.merge_inherit(inherit)

    def merge_inherit(self, inherit: InheritConfig):
        inherit_lang_info = self.get_key(inherit.value.split(".", 1)[-1])
        for inherit_key, inherit_value in inherit_lang_info.items():
            if self.get(inherit_key):
                if isinstance(inherit_value, list):
                    self[inherit_key] = list(set(self[inherit_key] + inherit_value))
                elif isinstance(inherit_value, dict):
                    self[inherit_key] = self[inherit_key].update(inherit_value)
            else:
                self[inherit_key] = inherit_value
            keys_cur = self.get(f"{inherit.cspath}:loadedKeys", [])
            if not keys_cur:
                self[f"{inherit.cspath}:loadedKeys"] = keys_cur
            if inherit_key not in keys_cur:
                keys_cur.append(inherit_key)

    def get_package_format_json(self, package_name):
        pacakge_json = self.get_package(package_name)
        return format_package_json(pacakge_json)

    def set_arch(self, arch="aarch64"):
        self.arch = arch
        self["arch"] = arch


config_space = ConfigSpace()
inherit_config = {}
config_space.arch = platform.machine()
