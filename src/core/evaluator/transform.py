# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os
import yaml


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


def load_yaml(file):
    if not os.path.exists(file):
        return {}
    with open(file) as f:
        return yaml.safe_load(f)


def transform_key_with_use_configure(key, value, fspath):
    from src.core.config_space import config_space
    if "useConfigureFlags" not in key:
        return "", {}
    keys = key.split(".useConfigureFlags.")
    if len(keys) < 2:
        return "", {}
    prefix = keys[0]
    flags = keys[1].split(".", maxsplit=1)
    if len(flags) < 2:
        return "", {}
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

    value_key = {
        "value": value,
        "fspath": fspath,
        "when": "%%use.{}".format(use_config_flag)
    }
    real_key = prefix + "." + suffix
    if suffix.endswith('enable'):
        real_key = f"{prefix}.env.useConfigureFlags"
    elif suffix.endswith('disable'):
        real_key = f"{prefix}.env.useConfigureFlags"
        value_key["when"] = "{{ " + "not %%use.{}".format(use_config_flag) + " }}"

    config_space_key = prefix + ".use." + use_config_flag + ":default"
    config_space[config_space_key] = flag

    return real_key, value_key


def transform_key_with_when(key, value, fspath):
    if "when" not in key:
        return "", {}
    keys = key.split()
    real_key = keys[0]
    use_config_flag = keys[2]
    if use_config_flag.startswith("+"):
        when = "%%use.{}".format(use_config_flag[1:])
    elif use_config_flag.startswith("-"):
        when = "{{ " + "not %%use.{}".format(use_config_flag[1:]) + " }}"
    else:
        when = "%%use.{}".format(use_config_flag)
    value_key = {
        "value": value,
        "fspath": fspath,
        "when": when
    }
    return real_key, value_key


def transform_key_with_iuse(key, value):
    from src.core.config_space import config_space
    if not key.endswith(".iuse"):
        return {}
    package = key[:-5]
    res = {}
    keys = config_space.get_key("use.{}:loadedKeys".format(value))
    for k in keys:
        use_value = config_space.get_key("use.{}.{}".format(value, k))
        use_configure = "{}.useConfigureFlags.{}.{}".format(package, value, k)
        real_key, v = transform_key_with_use_configure(use_configure, use_value, None)
        res[real_key] = v
    return res


def transform_key_default(key, value, fspath):
    key_c, value_c = transform_key_with_use_configure(key, value, fspath)
    if key_c == "":
        key_c, value_c = transform_key_with_when(key, value, fspath)
    else:
        key_c, value_c = transform_key_with_when(key_c, value_c, fspath)
    if key_c == "":
        return key, {"value": value,
                     "fspath": fspath,
                     "when": None}
    else:
        return key_c, value_c
