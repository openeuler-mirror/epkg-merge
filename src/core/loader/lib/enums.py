# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
from enum import Enum


# Enum of config files
class Config(Enum):
    MAIN_CONFIG = "config.yaml"
    INDEX = "default.yaml"


# Enum of keys in main config file
class MainConfigKey(Enum):
    LAYERS = "layers"


# Enum of keys in pkgs index config file
class IndexConfigKey(Enum):
    CONFIG_FILES_PATTERN = "configFilesPattern"
    REGISTER_FOR_FILE = "registerConfigSpaceForEachFile"
    INCLUDE_PHASE = "includePhase"
    INCLUDE_RUNTIME_PHASE = "includeRuntimePhase"
    INCLUDE = "include"


# Enum of directory names
class Directory(Enum):
    PKGS = "pkgs"
    LIBS = "libs"
    USE = "use"
    TYPES = "types"
    RPMRC = "rpmrc"
    LANG = "lang"


# Enum of partner of import config
class ImportConfig(Enum):
    PKG_GET = "(\$\{\{pkg\.get\(([-\\'\\\"\w.]+)\)}})"
    PKG_KEY = "(\$\{\{pkg\[([-\'\"\w.]+)]}})"
    PKG_HAS = "(\$\{\{pkg\.has\(([-\\'\\\"\w.]+)\)}})"
    TOP_KEY = "(\$\{\{top\[[\\'\\\"]([-\\'\\\"\w.]+)[\\'\\\"]]}})"
