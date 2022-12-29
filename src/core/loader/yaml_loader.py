# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os

import yaml

from src.core.evaluator import transform
from src.core.loader.lib.enums import IndexConfigKey
from src.core.loader.lib.load_helper import expand_yaml
from src.core.loader.load_exception import LoadException


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
        result = self.load_inherit(result)
        for k, v in result.items():
            actual_keys = config_space.add_key(k, v, self._fspath, None)
            if ":" in k:
                continue
            for actual_key in actual_keys:
                config_space.setdefault(f"{self._cspath}:loadedKeys", set()).add(actual_key)

    def load_inherit(self, package_info):
        from src.core.config_space import config_space
        final_package_info = {}
        for k, v in package_info.items():
            if k != f"{self._cspath}.inherit":
                if k in final_package_info:
                    final_package_info.pop(k)
                final_package_info[k] = v
                continue
            inherit_package = v.split(".")[1]
            inherit_package_info = config_space.get_package(inherit_package)
            inherit_key = v.replace(f"pkgs.{inherit_package}", "")
            for inherit_k, inherit_v in inherit_package_info.items():
                if inherit_key and inherit_key not in inherit_k:
                    continue
                final_package_info[f"{self._cspath}.{inherit_k}"] = inherit_v
        return final_package_info

    @staticmethod
    def load_include(configs):
        final_configs = {}
        for k, v in configs.items():
            if k != "include":
                if k in final_configs:
                    final_configs.pop(k)
                final_configs[k] = v
                continue
            include = yaml.safe_load(open(v, encoding="utf-8"))
            final_configs.update(include)
        return final_configs

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
                        actual_keys = config_space.add_key(k, v, self._fspath, None)
                        if ":" in k:
                            continue
                        for actual_key in actual_keys:
                            config_space.setdefault(f"{self._cspath}:loadedKeys", set()).add(actual_key)

    def _register_fspath_info(self) -> None:
        from src.core.config_space import config_space
        config_space[f'files."{self._fspath}".cspath'] = self._cspath
