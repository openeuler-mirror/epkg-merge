# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

from src.core.loader.yaml_loader import YamlLoader
from src.core.evaluator.merge import merge_values
from src.core.evaluator.transform import transform_key_default
from src.core.common import format_package_json

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
    fspath_list = None
    while True:
        raw_key = temp_key
        fspath_list = config_space.get(f"{raw_key}:fspath")
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

    @make_synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = dict.__new__(cls, *args, **kwargs)
        return cls.instance

    def get_key_value(self, key):
        value = self.get(key)
        if value is not None:
            return value
        values = self.get(f"{key}:values")
        if values is not None:
            value = merge_values(key)
            if not check_value(key, value):
                return None
            self[key] = value
            return value
        return None

    def get_key(self, key):
        value = self.get_key_value(key)
        if value is not None:
            return value

        raw_key, fspath_list = get_key_fspath(key)
        fspath_set = set()
        if type(fspath_list) is list:
            fspath_set = set(fspath_list)
        fspath_set_not_loaded = fspath_set - ConfigSpace.fspath_loaded
        if not fspath_set_not_loaded:
            return None
        for fspath in fspath_set_not_loaded:
            # 文件已加载，但没有这个key
            YamlLoader(raw_key, fspath).load()
            ConfigSpace.fspath_loaded.add(fspath)
        value = self.get_key_value(key)
        if value:
            return value

        return False

    def add_key(self, key, value, fspath, when):
        # key_c, value_c = transform_key_with_use_configure(key, value, fspath)
        key_info = transform_key_default(key, value, fspath)
        real_keys = []
        for k, v in key_info:
            real_keys.append(k)
            self.setdefault(f"{k}:values", []).append(v)
        return real_keys

    def get_package(self, package_name):
        pre_name = f"pkgs.{package_name}"
        # keys = self.keys()
        package_info = {}
        self.get_key(pre_name)
        loaded_keys = config_space.get_key(f"pkgs.{package_name}:loadedKeys")
        for key in loaded_keys:
            if "useConfigureFlags" in key:
                continue
            value = config_space.get_key(key)
            short_key = key.replace(f"{pre_name}.", "")
            package_info[short_key] = value

        sorted_keys = sorted(package_info.keys())

        package_info_sorted = {}
        for key in sorted_keys:
            package_info_sorted[key] = package_info[key]
        return package_info_sorted

    def get_package_format_json(self, package_name):
        pacakge_json = self.get_package(package_name)
        return format_package_json(pacakge_json)


config_space = ConfigSpace()
