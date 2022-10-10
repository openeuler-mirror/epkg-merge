# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os

import yaml

from src.core.loader.lib.load_helper import expand_yaml
from src.core.loader.load_exception import LoadException


class YamlLoader:

    def __init__(self, cspath: str, fspath: str) -> None:
        if not os.path.isfile(fspath):
            raise LoadException(f"'{fspath}' is not a file, fail to load '{cspath}'")

        self._cspath = cspath
        self._fspath = fspath

    def load(self):
        self.load_yaml()
        self.load_include_and_inherit()
        self.register_fspath_info()

    def load_yaml(self):
        configs = yaml.safe_load(open(self._fspath, encoding="utf-8"))
        result = expand_yaml(configs, self._cspath)
        for k, v in result.items():
            from src.core.config_space import config_space
            config_space.set_key(k, v, self._fspath, None)

    def load_include_and_inherit(self):
        ...

    def register_fspath_info(self):
        from src.core.config_space import config_space
        config_space.set_key(f'files."{self._fspath}".cspath', self._cspath, self._fspath, None)
