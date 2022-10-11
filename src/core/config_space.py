# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

from src.core.loader.yaml_loader import YamlLoader
from src.core.evaluator.merge import merge_values


def make_synchronized(func):
    import threading
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


def get_key_fspath(key):
    raw_key = ".".join(key.split(".")[:2])
    fspath_list = config_space.get(f"{raw_key}:fspath")
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
        values = self.get(f"{key}:values")
        if values is not None:
            value = merge_values(key)
            # if not check_value(key, value):
            #     pass # 告警
            #     return None
            self[key] = value
            return value
        return None

    def get_key(self, key):
        value = self.get(key)
        if value is not None:
            return value

        value = self.get_key_value(key)
        if value:
            return value

        raw_key, fspath_list = get_key_fspath(key)
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
        self.setdefault(f"{key}:values", [])
        self[f"{key}:values"].append({
            "value": value,
            "fspath": fspath,
            "when": when
        })

    def get_package(self, package_name):
        pre_name = f"pkgs.{package_name}"
        keys = self.keys()
        package_info = {}
        self.get_key(pre_name)
        for key in keys:
            if pre_name not in key:
                continue
            if ":fspath" in key:
                continue
            if ":values" in key:
                raw_key = key.replace(":values", "")
                value = self.get_key(raw_key)
                short_key = raw_key.replace(pre_name, "")
                package_info[short_key] = value
        return package_info


config_space = ConfigSpace()
