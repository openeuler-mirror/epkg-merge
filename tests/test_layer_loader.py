# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

from src.core.loader.layer_loader import LayerLoader
from src.core.loader.yaml_loader import YamlLoader
from src.core.config_space import config_space
import os


curdir = os.path.abspath(os.curdir)

config_file = os.path.join(curdir, "demo/config.yaml")
LayerLoader(config_file).load()

name = config_space.get_key("pkgs.kernel.name")
print(name)