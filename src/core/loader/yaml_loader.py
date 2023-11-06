# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os
import yaml
from src.core.evaluator import transform
from src.core.loader.lib.enums import IndexConfigKey
from src.core.loader.lib.load_helper import expand_yaml
from src.core.loader.load_exception import LoadException
from src.core.lib.exclude_key import is_strategy_key

class YamlLoader:

    def __init__(self, cspath: str, fspath: str) -> None:
        if not os.path.isfile(fspath):
            raise LoadException(f"'{fspath}' is not a file, fail to load '{cspath}'")

        self._cspath = cspath
        self._fspath = fspath

    def load(self) -> None:
        self._load_yaml()
        self._load_include_and_inherit()
        self._register_fspath_info()

    def _load_yaml(self) -> None:
        from src.core.config_space import config_space
        configs = yaml.safe_load(open(self._fspath, encoding="utf-8"))
        configs = self.load_include(configs)
        result = expand_yaml(configs, self._cspath)
        self.save_inherit_item(result)
        for k, v in result.items():
            actual_keys = config_space.add_key(k, v, self._fspath)
            if is_strategy_key(k):
                continue
            for actual_key in actual_keys:
                keys_cur = config_space.get(f"{self._cspath}:loadedKeys", [])
                if not keys_cur:
                    config_space[f"{self._cspath}:loadedKeys"] = keys_cur
                if actual_key not in keys_cur:
                    keys_cur.append(actual_key)

    def save_inherit_item(self, items: dict):
        from src.core.config_space import inherit_config
        for k, v in items.items():
            if ".inherit" in k:
                inherit_config[k] = {
                    "value": v,
                    "fspath": self._fspath,
                    "cspath": self._cspath
                }

    @staticmethod
    def load_include(configs):
        final_configs = {}
        for k, v in configs.items():
            if k != "include":
                YamlLoader.sequential_update(k, v, final_configs)
                continue
            for include in v.split(","):
                include_info = yaml.safe_load(open(include, encoding="utf-8"))
                final_configs.update(include_info)
        return final_configs

    @staticmethod
    def sequential_update(k, v, original_dict):
        if k in original_dict:
            original_dict.pop(k)
        original_dict[k] = v
        return original_dict

    def _load_include_and_inherit(self) -> None:
        from src.core.config_space import config_space
        include_item_transform_dict = {
            IndexConfigKey.INCLUDE.value: "load_yaml",
            IndexConfigKey.INCLUDE_PHASE.value: "transform_include_phase",
            IndexConfigKey.INCLUDE_RUNTIME_PHASE.value: "transform_include_phase",
        }
        for item, func in include_item_transform_dict.items():
            if include := config_space.get_key(f'files."{self._fspath}".{item}'):
                for f in include.split():
                    transform_result = getattr(transform, func)(os.path.join(os.path.dirname(self._fspath), f))
                    result = expand_yaml(transform_result, self._cspath)
                    for k, v in result.items():
                        actual_keys = config_space.add_key(k, v, self._fspath)
                        if is_strategy_key(k):
                            continue
                        for actual_key in actual_keys:
                            keys_cur = config_space.get(f"{self._cspath}:loadedKeys", [])
                            if not keys_cur:
                                config_space[f"{self._cspath}:loadedKeys"] = keys_cur
                            if actual_key not in keys_cur:
                                keys_cur.append(actual_key)

    def _register_fspath_info(self) -> None:
        from src.core.config_space import config_space
        config_space[f'files."{self._fspath}".cspath'] = self._cspath
