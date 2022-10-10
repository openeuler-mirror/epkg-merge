# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
from enum import Enum


# Enum of config files
class Config(Enum):
    MAIN_CONFIG = "config.yaml"
    INDEX = "index.yaml"


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
    LIB = "lib"
    USE = "use"
