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
        result = expand_yaml(configs, self._cspath)
        for k, v in result.items():
            config_space.set_key(k, v, self._fspath, None)

    def _load_include_and_inherit(self) -> None:
        from src.core.config_space import config_space
        include_item_transform_dict = {
            IndexConfigKey.INCLUDE.value: "transform_include_phase",
            IndexConfigKey.INCLUDE_PHASE.value: "transform_include_phase",
            IndexConfigKey.INCLUDE_RUNTIME_PHASE.value: "load_yaml",
        }
        for item, func in include_item_transform_dict:
            if include := config_space.get_key(f'files."{self._fspath}".include.{item}'):
                for f in include.split():
                    transform_result = getattr(transform, func)(os.path.join(os.path.dirname(self._fspath), f))
                    result = expand_yaml(transform_result, self._cspath)
                    for k, v in result.items():
                        config_space.set_key(k, v, self._fspath, None)

    def _register_fspath_info(self) -> None:
        from src.core.config_space import config_space
        config_space.set_key(f'files."{self._fspath}".cspath', self._cspath, self._fspath, None)
