# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import yaml
import argparse


def handle_load(file):
    from src.core.loader.yaml_loader import YamlLoader
    YamlLoader.load(file)


def handle_package(package):
    from src.core.config_space import config_space
    return config_space.get_package(package)


def handle_output(content, output):
    if not content:
        return
    if not output:
        output = "./package.yaml"
    f = open(output, 'w')
    yaml.dump(content, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="the configuration file to be parsed")
    parser.add_argument("-p", "--package", help="the parsed package name")
    parser.add_argument("-o", "--output", help="which file the output is redirected to")
    args = vars(parser.parse_args())
    if args["config_file"]:
        handle_load(args["config_file"])
    package_info = handle_package(args["package"])
    handle_output(package_info, args["output"])


if __name__ == '__main__':
    main()
