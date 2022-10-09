# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os


def transform_include_phase(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        content = f.readlines()
        return parse_shell_file(content)


def parse_shell_file(content):
    functions = {}
    function_name = ""
    function_content = ""
    for line in content:
        _line = line.rstrip()
        if function_name:
            if _line == "{":
                continue
            if _line == "}":
                functions[function_name] = function_content
                function_name, function_content = "", ""
                continue
            function_content += line
        else:
            function_name = get_shell_function_name(line)
    return functions


def get_shell_function_name(line):
    if line.startswith("function"):
        name = line.strip().split()[1]
        return parse_function_name(name)
    if len(line.split()) > 2:
        return ""
    if "()" not in line:
        return ""
    name = line.split()[0]
    return parse_function_name(name)


def parse_function_name(name):
    if name.endswith("{"):
        name = name[0:-1]
    if name.endswith("()"):
        name = name[0:-2]
    return name
