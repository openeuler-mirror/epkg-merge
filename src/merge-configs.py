#!/usr/bin/python
# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import sys
import argparse
import os
import logging

sys.path.append(os.path.abspath("."))

from src.log import log
from src.core.interpreter.interpreter import StartUp
from src.cli.cli_handler import handle_load, handle_output, handle_package


def main():
    from src.core.config_space import config_space
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config_file", help="the configuration file to be parsed")
    parser.add_argument("-p", "--packages", help="the parsed packages， use -p 'A B' to specify multiple packages")
    parser.add_argument("-o", "--output", help="which dir the output is redirected to")
    parser.add_argument("-d", "--debug", action="store_true", help="output the run log to the terminal")
    args = vars(parser.parse_args())
    if args["debug"]:
        log.addHandler(logging.StreamHandler())
    if args["config_file"]:
        handle_load(args["config_file"])
        StartUp.startup(config_space)
    packages = []
    if args["packages"]:
        packages = args["packages"].split()
    for package in packages:
        package_info = handle_package(package, config_space)
        handle_output(package, package_info, args["output"])


if __name__ == '__main__':
    main()
