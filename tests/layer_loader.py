# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
from src.log import log
import logging
console_handler = logging.StreamHandler()
console_handler.setLevel(level="WARNING")
log.addHandler(console_handler)

from src.core.loader.layer_loader import LayerLoader
from src.core.config_space import config_space
import os
from src.core.interpreter.interpreter import StartUp
from src.core.common import format_package_json

current_dir = os.path.abspath(os.curdir)
config_file = os.path.join(current_dir, "demo/config.yaml")
LayerLoader(config_file).load()
StartUp.startup(config_space)
config_space.set_arch("x86_64")
p = "glibc"
x = config_space.get_package_format_json(p)
import yaml


with open(f"./merge/{p}.yaml", "w+") as f:
    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
    def repr_str(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
        return dumper.org_represent_str(data)
    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)
    # yaml.safe_dump(x, sys.stdout)

    yaml.safe_dump(x, f, allow_unicode='uft-8', sort_keys=False)