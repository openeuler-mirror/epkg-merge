#!/usr/bin/python
# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import sys
import argparse
import os
import logging
import json
import platform

sys.path.append(os.path.abspath("."))

from src.log import log
from src.core.interpreter.interpreter import StartUp
from src.cli.cli_handler import handle_load, handle_output, handle_package
import traceback

def main():
    from src.core.config_space import config_space
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="the configuration file to be parsed")
    parser.add_argument("-p", "--packages", help="the parsed packages， use -p 'A B' to specify multiple packages")
    parser.add_argument("-o", "--output", help="which dir the output is redirected to")
    parser.add_argument("-d", "--debug", action="store_true", help="output the run log to the terminal")
    parser.add_argument("-l", "--list-features", help="displays user configuration information")
    parser.add_argument("-a", "--arch", help="set merge arch")
    args = vars(parser.parse_args())
    list_features_info = {}
    arch = args.get("arch", platform.machine())
    config_space.set_arch(arch)
    out_path = os.path.join(os.getcwd(),"merge")
    if args["output"]:
        out_path = args["output"]
    if args["list_features"]:
        for k in args["list_features"].split(","):
            list_features_info[k] = {}

    console_handler = logging.StreamHandler()
    console_format = logging.Formatter("[%(levelname)s][%(filename)s][%(lineno)s]: %(message)s")
    console_handler.setFormatter(console_format)
    console_handler.setLevel(level="WARNING")
    if args["debug"]:
        console_handler.setLevel(level="INFO")
    log.addHandler(console_handler)

    if args["config_file"]:
        handle_load(args["config_file"], arch)
        StartUp.startup(config_space)
    if args["packages"]:
        packages = args["packages"].split()
    else:
        packages = config_space["allPkgs"]
    packages = sorted(packages)
    for package in packages:
        log.info(f"==========parse package {package}===============")
        package_info = handle_package(package, config_space)
        if not list_features_info:
            handle_output(package, package_info, out_path)
            continue
        for k, v in package_info.items():
            if "use." in k:
                k = k.replace("use.", "")
                list_features_info[package][k] = v

    for k, v in list_features_info.items():
        print(k)
        print(json.dumps(v))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_stack()
        print(e)
