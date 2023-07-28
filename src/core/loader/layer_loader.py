# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os
import re
import threading
from typing import Any, Dict, List
import yaml
from src.core.loader.lib.enums import Config, MainConfigKey, Directory, IndexConfigKey
from src.core.loader.lib.load_helper import expand_yaml
from src.core.loader.load_exception import LoadException
from src.log import log


class LayerLoader:
    __LOCK = threading.Lock()

    def __init__(self, config_file: str = Config.MAIN_CONFIG.value) -> None:
        if not os.path.isfile(config_file):
            raise LoadException(f"Main config '{config_file}' is not a file")

        self._config_file = config_file
        self._dir_name = os.path.dirname(os.path.abspath(config_file))

    def load(self, arch) -> None:
        with self.__LOCK:
            log.info(f"Loading layers with main config: '{self._config_file}'")
            layers: Dict[str, List[str]] = yaml.safe_load(open(self._config_file, encoding="utf-8"))
            if not layers.get(str(MainConfigKey.LAYERS.value)):
                raise LoadException(
                    f"Invalid main config: can't find yaml key '{MainConfigKey.LAYERS.value}' or empty value")

            for layer in layers.get(str(MainConfigKey.LAYERS.value)):
                _LayerConfigLoader(layer, os.path.join(self._dir_name, layer), arch).load()
            log.info(f"Successfully load layers with main config: '{self._config_file}'")


class _LayerConfigLoader:
    def __init__(self, layer: str, layer_path: str, target_arch: str) -> None:
        if not os.path.isdir(layer_path):
            raise LoadException(f"The path of layer '{layer}' [{layer_path}] is not a directory")

        self._layer = layer
        self._layer_path = layer_path
        self.arch = target_arch
        self.index_config = {
            "configFilesPattern": r"(?P<_pkgname>[-0-9a-zA-Z_.]+)(/|\\)(package\.yaml)",
            "registerConfigSpaceForEachFile": {"pkgs.${{pkg._basename}}:fspath": "${{pkg._filepath}}",
            "files.\"${{pkg._filepath}}\"": {
                "name": "${{pkg._basename}}", # can catch spell error if conflict with the name defined in yaml
                "docType": "base",
                "includePhase": "phase.sh",
                "includeRuntimePhase": "runtimePhase.sh runtimePhase.lua",
                "include": "versions.yaml files.yaml defineFlags.yaml",
                ":referAttrs": "types.package",
                "meta:referAttrs": "types.package.meta",
                "phase:referAttrs": "types.package.phase",
                "runtimePhase:referAttrs": "types.package.runtimePhase"}
            }
        }

    def load(self) -> None:
        log.info(f"Loading layer: '{self._layer}' with layer path: '{self._layer_path}'")
        self._load_languages()
        self._load_pkgs()
        self._load_python_libs()
        self._load_use()
        self._load_types()
        self._load_rpmrc()
        log.info(f"Successfully load layer: '{self._layer}' with layer path: '{self._layer_path}'")

    def _load_pkgs(self) -> None:
        pkgs_dir = os.path.join(self._layer_path, str(Directory.PKGS.value))
        if not os.path.isdir(pkgs_dir):
            return

        self._load_pkgs_index_yaml(pkgs_dir)

    def _load_pkgs_index_yaml(self, pkgs_dir: str) -> None:
        index_config = self.index_config
        pattern = index_config.get(str(IndexConfigKey.CONFIG_FILES_PATTERN.value))
        if not pattern:
            raise LoadException(f"'{IndexConfigKey.CONFIG_FILES_PATTERN.value}' "
                                f"of pkgs index file in layer '{self._layer}' is empty")

        for pkg in [d for d in os.listdir(pkgs_dir) if os.path.isdir(os.path.join(pkgs_dir, d))]:
            pkg_config = None
            for f in os.listdir(os.path.join(pkgs_dir, pkg)):
                if re.match(pattern, os.path.join(pkg, f)):
                    pkg_config = os.path.join(pkgs_dir, pkg, f)
                    break

            if not pkg_config:
                log.error(f"layer '{self._layer}' lacks of {pkg}.yaml")
                continue

            _ElementConfigLoader(pkg, pkg_config, index_config).load()
            from src.core.config_space import config_space
            config_space.setdefault("allPkgs", set()).add(pkg)

    def _load_python_libs(self) -> None:
        lib_path = os.path.join(self._layer_path, str(Directory.LIBS.value))
        if not os.path.isdir(lib_path):
            return

        from src.core.config_space import config_space
        for f in os.listdir(lib_path):
            if re.match(r".*\.py", f):
                config_space.setdefault("libs", []).append(os.path.join(lib_path, f))

    def _load_use(self) -> None:
        use_dir = os.path.join(self._layer_path, str(Directory.USE.value))
        if not os.path.isdir(use_dir):
            return

        self._load_use_index_yaml(use_dir)

    def _load_use_index_yaml(self, use_dir: str) -> None:
        index_config = self.index_config
        pattern = index_config.get(str(IndexConfigKey.CONFIG_FILES_PATTERN.value))
        if not pattern:
            raise LoadException(f"'{IndexConfigKey.CONFIG_FILES_PATTERN.value}' "
                                f"of use index file in layer '{self._layer}' is empty")

        for use in [f for f in os.listdir(use_dir) if
                    os.path.isfile(os.path.join(use_dir, f)) and re.match(pattern, f) and f != str(Config.INDEX.value)]:
            _ElementConfigLoader(".".join(use.split(".")[:-1]), os.path.join(use_dir, use), index_config).load()

    def _load_types(self) -> None:
        types_path = os.path.join(self._layer_path, str(Directory.TYPES.value))
        if not os.path.isdir(types_path):
            return

        from src.core.config_space import config_space
        for f in os.listdir(types_path):
            if re.match(r".*\.yaml", f):
                result = expand_yaml(yaml.safe_load(open(os.path.join(types_path, f), encoding="utf-8")))
                for k, v in result.items():
                    config_space[k] = v

    def _load_rpmrc(self) -> None:
        rpmrc_path = os.path.join(self._layer_path, str(Directory.RPMRC.value))
        if not os.path.isdir(rpmrc_path):
            return
        from src.core.config_space import config_space
        rpmrc_path_list = [
            "rpmrc.yaml",
            os.path.join("openEuler", "rpmrc.yaml"),
            os.path.join("platform", "{0}-linux".format(self.arch), "rpmrc.yaml")
        ]
        for rpmrc_file in rpmrc_path_list:
            rpmrc_file_path = os.path.join(rpmrc_path, rpmrc_file)
            if not os.path.exists(rpmrc_file_path):
                log.warn("Don't have this arch in rpmrc")
                continue
            result = expand_yaml(yaml.safe_load(open(rpmrc_file_path, encoding="utf-8")))
            for k, v in result.items():
                rpmrc_key = "rpmGlobal.{}".format(k)
                config_space.add_key(rpmrc_key, v, rpmrc_file_path)
        if os.path.exists(os.path.join(rpmrc_path, "macros.d")):
            for method in os.listdir(os.path.join(rpmrc_path, "macros.d")):
                if method.endswith(".yaml"):
                    method_rpmrc = os.path.join(rpmrc_path, "macros.d", method)
                    result = expand_yaml(yaml.safe_load(open(method_rpmrc, encoding="utf-8")))
                    for k, v in result.items():
                        rpmrc_key = "rpmGlobal.{}".format(k)
                        config_space.add_key(rpmrc_key, v, method_rpmrc)

    def _load_languages(self):
        language_path = os.path.join(self._layer_path, str(Directory.LANG.value))
        if not os.path.isdir(language_path):
            return
        from src.core.config_space import config_space
        language_list = os.listdir(language_path)
        for language_yaml in language_list:
            language_yaml_path = os.path.join(language_path, language_yaml)
            language_name = language_yaml.split(".")[0]
            result = expand_yaml(yaml.safe_load(open(language_yaml_path, encoding="utf-8")))
            for k, v in result.items():
                language_key = "lang.{0}.{1}".format(language_name, k)
                config_space.add_key(language_key, v, language_yaml_path)


class _ElementConfigLoader:
    IMPLICIT_FIELDS = {
        "basename": "${{pkg._basename}}",
        "filepath": "${{pkg._filepath}}",
        "dirname": "${{pkg._dirname}}",
        "filename": "${{pkg._filename}}",
    }

    def __init__(self, element: str, element_config_path: str, index_config: Dict[str, Any]) -> None:
        self._implicit_fields = {
            self.IMPLICIT_FIELDS["basename"]: element,
            self.IMPLICIT_FIELDS["filepath"]: element_config_path,
            self.IMPLICIT_FIELDS["dirname"]: os.path.dirname(element_config_path),
            self.IMPLICIT_FIELDS["filename"]: os.path.basename(element_config_path),
        }
        self._index_config = index_config

    def load(self) -> None:
        from src.core.config_space import config_space
        configs: Dict[str, Any] = self._index_config.get(str(IndexConfigKey.REGISTER_FOR_FILE.value))
        result = expand_yaml(configs, implicit_fields=self._implicit_fields)
        for k, v in result.items():
            if "fspath" in k:
                config_space.setdefault(k, []).append(v)
            else:
                config_space[k] = v
