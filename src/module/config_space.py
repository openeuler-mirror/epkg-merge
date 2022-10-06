# Copyright (c) 2022 Huawei Technologies Co.,Ltd. All rights reserved.
#
# StratoVirt is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan
# PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http:#license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from src.module.loader.layer_loader import LayerLoader
from src.module.loader.yaml_loader import YAMLLoader
from src.module.evaluator.merge import merge_values
from src.module.evaluator.check import check_value


def make_synchronized(func):
    import threading
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


def get_key_fspath(key):
    return key

class ConfigSpace(dict):
    instance = None
    fspath_readed = set()

    @make_synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = dict.__new__(cls, *args, **kwargs)
        return cls.instance

    def get_key_value(self, key):
        values = self.get(f"{key}:values")
        if values is not None:
            value = merge_values(values)
            if not check_value(key, value):
                pass # 告警
                return None
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

        fspath = get_key_fspath(key)
        if fspath in ConfigSpace.fspath_readed:
            # 文件已加载，但没有这个key 
            return None

        YAMLLoader.load(key, fspath)

        value = self.get_key_value(key)
        if value:
            return value

        return False

    def set_key(self, key, value, fspath, when):
        self.setdefault(f"{key}:values",[])
        self[f"{key}:values"].append({
            "value": value,
            "fspath": fspath,
            "when": when
        })

config_space = ConfigSpace()
