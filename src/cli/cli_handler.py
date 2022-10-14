# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import os
import shutil
import yaml
from src.core.config_space import ConfigSpace

def handle_load(file):
    from src.core.loader.layer_loader import LayerLoader
    LayerLoader(file).load()


def handle_package(package, config_space):
    return config_space.get_package_format_json(package)


def handle_output(package_name, content, output):
    if not content:
        return
    if not output:
        output = "./" + package_name
    else:
        output = output + "/" + package_name
    # $output/$package_name.yaml
    if not os.path.exists(output):
        os.makedirs(output)
    file = output + "/" + package_name + ".yaml"
    with open(file, "w") as f:
        yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

        def repr_str(dumper, data):
            if '\n' in data:
                return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
            return dumper.org_represent_str(data)

        yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)
        yaml.safe_dump(content, f, allow_unicode='uft-8')

    os.system(f"python3 ./src/tools/transition/openEulerTransitionMain.py -t {file}")

    for path in ConfigSpace.fspath_loaded:
        package_path, file_name = os.path.split(path)
        if f"{package_name}.yaml" == file_name:
            sub_files = os.listdir(package_path)
            for sub_file in sub_files:
                if sub_file.endswith(".yaml") or sub_file.endswith(".spec"):
                    continue
                src_path = os.path.join(package_path, sub_file)
                shutil.copy(src_path, output)