# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os
import re
from typing import Any, Dict, List

import yaml

from src.core.loader.lib.enums import Config, MainConfigKey, Directory, IndexConfigKey
from src.core.loader.lib.load_helper import expand_yaml
from src.core.loader.load_exception import LoadException


class LayerLoader:
    def __init__(self, config_file: str = Config.MAIN_CONFIG.value) -> None:
        if not os.path.isfile(config_file):
            raise LoadException(f"Main config '{config_file}' is not a file")

        self._config_file = config_file
        self._dir_name = os.path.dirname(os.path.abspath(config_file))

    def load(self) -> None:
        layers: Dict[str, List[str]] = yaml.safe_load(open(self._config_file, encoding="utf-8"))
        if not layers.get(str(MainConfigKey.LAYERS.value)):
            raise LoadException(
                f"Invalid main config: can't find yaml key '{MainConfigKey.LAYERS.value}' or empty value")

        for layer in layers.get(str(MainConfigKey.LAYERS.value)):
            LayerConfigLoader(layer, os.path.join(self._dir_name, layer)).load()


class LayerConfigLoader:
    def __init__(self, layer: str, layer_path: str) -> None:
        if not os.path.isdir(layer_path):
            raise LoadException(f"The path of layer '{layer}' [{layer_path}] is not a directory")

        self._layer = layer
        self._layer_path = layer_path

    def load(self) -> None:
        self._load_pkgs()

    def _load_pkgs(self) -> None:
        pkgs_dir = os.path.join(self._layer_path, str(Directory.PKGS.value))
        if not os.path.isdir(pkgs_dir):
            return

        self._load_index_yaml(pkgs_dir)

    def _load_index_yaml(self, pkgs_dir: str) -> None:
        index_yaml = os.path.join(pkgs_dir, str(Config.INDEX.value))
        if not os.path.isfile(index_yaml):
            raise LoadException(f"Index file of layer '{self._layer}' is missing")

        index_config: Dict[str, Any] = yaml.safe_load(open(index_yaml, encoding="utf-8"))
        pattern = index_config.get(str(IndexConfigKey.CONFIG_FILES_PATTERN.value))
        if not pattern:
            raise LoadException(f"'{IndexConfigKey.CONFIG_FILES_PATTERN.value}' of layer '{self._layer}' is empty")

        for pkg in [d for d in os.listdir(pkgs_dir) if os.path.isdir(os.path.join(pkgs_dir, d))]:
            pkg_config = None
            for f in os.listdir(os.path.join(pkgs_dir, pkg)):
                if re.match(pattern, os.path.join(pkg, f)):
                    pkg_config = os.path.join(pkgs_dir, pkg, f)
                    break

            if not pkg_config:
                print(f"warning: package '{pkg}' of layer '{self._layer}' lacks of main config")
                continue

            PkgLoader(pkg, pkg_config, index_config).load()


class PkgLoader:
    IMPLICIT_FIELDS = {
        "basename": "%%_basename",
        "filepath": "%%_filepath",
        "dirname": "%%_dirname",
        "filename": "%%_filename",
    }

    def __init__(self, pkg: str, pkg_config_path: str, index_config: Dict[str, Any]) -> None:
        self._implicit_fields = {
            self.IMPLICIT_FIELDS["basename"]: pkg,
            self.IMPLICIT_FIELDS["filepath"]: pkg_config_path,
            self.IMPLICIT_FIELDS["dirname"]: os.path.dirname(pkg_config_path),
            self.IMPLICIT_FIELDS["filename"]: os.path.basename(pkg_config_path),
        }
        self._index_config = index_config

    def load(self) -> None:
        configs: Dict[str, Any] = self._index_config.get(str(IndexConfigKey.REGISTER_FOR_FILE.value))
        result = expand_yaml(configs, implicit_fields=self._implicit_fields)
        for k, v in result.items():
            from src.core.config_space import config_space
            config_space.set_key(k, v, self._implicit_fields[self.IMPLICIT_FIELDS["filepath"]], None)

