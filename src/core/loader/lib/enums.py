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


# Enum of directory names
class Directory(Enum):
    PKGS = "pkgs"
