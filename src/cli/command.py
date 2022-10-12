# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import os
import yaml
import argparse

from src.core.py_interpreter.interpreter import startup


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


def main():
    from src.core.config_space import config_space
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="the configuration file to be parsed")
    parser.add_argument("-p", "--packages", help="the parsed packages， use -p 'A B' to specify multiple packages")
    parser.add_argument("-o", "--output", help="which dir the output is redirected to")
    args = vars(parser.parse_args())
    if args["config_file"]:
        handle_load(args["config_file"])
        startup(config_space)
    packages = []
    if args["packages"]:
        packages = args["packages"].split()
    for package in packages:
        package_info = handle_package(package, config_space)
        handle_output(package, package_info, args["output"])


if __name__ == '__main__':
    main()
