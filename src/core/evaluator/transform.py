# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os
import yaml
import copy

from src.core.constant.tokens import IF_TOKEN


def transform_include_phase(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        content = f.readlines()
        file_name = parse_file_name(file)
        if file.endswith(".lua"):
            return parse_lua_file(file_name, content)
        return parse_shell_file(file_name, content)

    
def parse_file_name(file):
    file = os.path.split(file)[-1]
    file_name = file.split(".")[0]
    return file_name


def parse_shell_file(file_name, content):
    functions = {}
    function_name = ""
    function_content = ""
    symbol_count = 0
    is_first_line = True
    rpm_macro_param = ""
    for line in content:
        _line = line.rstrip()
        if function_name:
            if is_first_line and symbol_count:
                is_first_line = False
                if "rpm_macro_param" in _line:
                    rpm_macro_param = _line.split(":")[-1].lstrip()
                    continue
            if _line == "{":
                function_content += line
                symbol_count += 1
                continue
            if symbol_count > 1 and _line.lstrip() == "}":
                function_content += line
                symbol_count -= 1
                continue
            if _line == "}":
                symbol_count -= 1
                if symbol_count:
                    function_content += line
                    continue
                functions[function_name] = function_content
                if rpm_macro_param:
                    function_param = function_name + ":" + "rpm_macro_param"
                    functions[function_param] = rpm_macro_param
                function_name, function_content, rpm_macro_param, is_first_line = "", "", "", True
                continue
            if "(){" in line or "() {" in line:
                symbol_count += 1
            function_content += line
        else:
            shell_function_name = get_shell_function_name(line)
            function_name = combinate_function_name(file_name, shell_function_name)
            if function_name and "{" in line:
                symbol_count += 1
    return functions


def parse_lua_file(file_name, content):
    functions = {}
    function_name = ""
    function_content = ""
    is_first_line = True
    rpm_macro_param = ""
    for line in content:
        _line = line.rstrip()
        if function_name:
            if is_first_line:
                is_first_line = False
                if "rpm_macro_param" in _line:
                    rpm_macro_param = _line.split(":")[-1].lstrip()
                    continue
            if _line != "end":
                function_content += line.lstrip()
                continue
            functions[function_name] = function_content
            if rpm_macro_param:
                function_param = function_name + ":" + "rpm_macro_param"
                functions[function_param] = rpm_macro_param
            function_name, function_content, rpm_macro_param, is_first_line = "", "", "", True
        else:
            shell_function_name = get_shell_function_name(line)
            function_name = combinate_function_name(file_name, shell_function_name)
    return functions


def combinate_function_name(file_name, function_name):
    if not function_name:
        return ""
    # 不是子包只需要拼接文件名
    if ":" not in function_name:
        return "{}.{}".format(file_name, function_name)
    # runtimePhase.sh下的函数： post:%{wxbasename}-devel
    # 解析成：subpackage.%{wxbasename}-devel.runtimePhase.post
    function_info = function_name.split(":", maxsplit=1)
    real_name = function_info[0]
    subpackage_name = function_info[1]
    return "subpackage.{}.{}.{}".format(subpackage_name, file_name, real_name)


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


def load_yaml(file):
    if not os.path.exists(file):
        return {}
    with open(file) as f:
        return yaml.safe_load(f)


def transform_key_with_defineFlags(key_dict: dict) -> dict:
    res = {}
    for key, value in key_dict.items():
        if "defineFlags" not in key:
            res[key] = value
            continue
        last_key = key.split("defineFlags.")[-1]
        if last_key.startswith("+"):
            real_key = key.replace(last_key, last_key[1:])
            value['value'] = True
            res[real_key] = value
        elif last_key.startswith("-"):
            real_key = key.replace(last_key, last_key[1:])
            value['value'] = False
            res[real_key] = value
        else:
            res[key] = value

    return res

def transform_key_with_use_configure(key_dict: dict) -> dict:
    res = {}
    for key, value in key_dict.items():
        if "useConfigureFlags" not in key:
            res[key] = value
            continue
        keys = key.split(".useConfigureFlags.")
        if len(keys) < 2:
            res[key] = value
            continue
        prefix = keys[0]
        flags = keys[1].split(".", maxsplit=1)
        if len(flags) < 2:
            res[key] = value
            continue
        use_config_flag = flags[0]
        suffix = flags[1]

        if use_config_flag.startswith("+"):
            flag = True
            use_config_flag = use_config_flag[1:]
        elif use_config_flag.startswith("-"):
            flag = False
            use_config_flag = use_config_flag[1:]
        else:
            flag = True

        value["when"] = "%%use.{}".format(use_config_flag)
        real_key = prefix + "." + suffix
        if suffix.endswith('enable'):
            real_key = f"{prefix}.env.useConfigureFlags"
        elif suffix.endswith('disable'):
            real_key = f"{prefix}.env.useConfigureFlags"
            value["when"] = "{{ " + "not %%use.{}".format(use_config_flag) + " }}"
        res[real_key] = value

        config_space_key = prefix + ".use." + use_config_flag + ":default"
        res[config_space_key] = {"value": flag}

    return res


def transform_key_with_when(key_dict: dict) -> dict:
    res = {}
    for key, value in key_dict.items():
        if IF_TOKEN not in key:
            res[key] = value
            continue
        keys = key.split(IF_TOKEN)
        real_key = keys[0].strip()
        when_statement = " ".join(keys[1:]).strip()
        when_statements = when_statement.split(" ")
        when = ""
        for flag in when_statements:
            if flag.startswith("+") or flag.startswith("-"):
                # format中{{ 会转换为{
                when = "{} ${{{{pkg.defineFlags.{}}}}}".format(when, flag)
            else:
                when = "{} {}".format(when, flag.strip())

        value["when"] = when.strip()
        res[real_key] = value
    return res


def transform_key_with_rpmWhen(key_dict: dict) -> dict:
    res = {}
    for key, value in key_dict.items():
        if "rpmWhen" not in key:
            res[key] = value
            continue
        elif "subpackage." not in key:
            res[key] = value
            continue
        key_info = key.split(" rpmWhen ")
        subpackage = key_info[0]
        find_out = False
        start = 1
        for i, item in enumerate(key_info[start:]):
            if "." in item:
                find_out = True
                start = i + 1
        if find_out:
            condition_info = key_info[start].split(".", maxsplit=1)
            if start > 1:
                condition_info = key_info[1: start] + condition_info
            condition = " rpmWhen ".join(condition_info[:-1])
            field = condition_info[-1]
            condition_value = copy.copy(value)
            res["{}.{}".format(subpackage, field)] = value
            res["{}:rpmWhen {}".format(subpackage, condition)] = condition_value
        else:
            res[subpackage] = value
            condition_value = copy.copy(value)
            rpm_condition = " rpmWhen ".join(key_info[1:])
            res["{}:rpmWhen {}".format(subpackage, rpm_condition)] = condition_value

    return res


def transform_key_with_iuse(key_dict: dict):
    from src.core.config_space import config_space
    res = {}
    for key, value in key_dict.items():
        if not key.endswith(".iuse"):
            res[key] = value
            continue
        package = key[:-5]
        keys = config_space.get_key("use.{}:loadedKeys".format(value))
        for k in keys:
            use_value = config_space.get_key("use.{}.{}".format(value, k))
            use_configure = "{}.useConfigureFlags.{}.{}".format(package, value, k)
            res[use_configure] = {"value": use_value}
    return res


def transform_key_default(key, value, fspath):
    transform_list = [
        # transform_key_with_defineFlags,
        transform_key_with_iuse,
        transform_key_with_use_configure,
        transform_key_with_when,
        transform_key_with_rpmWhen
    ]
    value_key = {
        "value": value,
        "fspath": fspath,
        "when": None
    }
    key_dict = {key: value_key}
    for func in transform_list:
        key_dict = func(key_dict)
    return key_dict
