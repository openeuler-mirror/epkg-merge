# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

from src.core.loader.yaml_loader import YamlLoader
from src.core.evaluator.merge import merge_values
from src.core.evaluator.transform import transform_key_default
from src.core.common import format_package_json
from src.core.evaluator.check import check_value
from src.core.constant.tokens import NOT_EXIST
from src.log import log
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


class ConfigSpace(dict):
    instance = None
    fspath_loaded = set()
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
        fspath_set = set()
        if type(fspath_list) is list:
            fspath_set = set(fspath_list)
        fspath_set_not_loaded = fspath_set - ConfigSpace.fspath_loaded
        if fspath_set_not_loaded:
            for fspath in fspath_set_not_loaded:
                # 文件已加载，但没有这个key
                YamlLoader(raw_key, fspath).load()
                ConfigSpace.fspath_loaded.add(fspath)
        value = self.get_key_value(key)
        return value

    def add_key(self, key, value, fspath):
        key_info = transform_key_default(key, value, fspath)
        for k, v in key_info.items():
            if ":" in k:
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
        loaded_keys = config_space.get_key(f"pkgs.{package_name}:loadedKeys")
        for key in loaded_keys:
            if "useConfigureFlags" in key:
                continue
            value = config_space.get_key(key)
            if value == NOT_EXIST:
                continue
            short_key = key.replace(f"{pre_name}.", "")
            package_info[short_key] = value

        return package_info

    def get_package_format_json(self, package_name):
        pacakge_json = self.get_package(package_name)
        return format_package_json(pacakge_json)

    def set_arch(self, arch="aarch64"):
        self.arch = arch


config_space = ConfigSpace()
config_space.arch = platform.machine()
