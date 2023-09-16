# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os
import re
from src.log import log
from src.core.loader.lib.config import *


def is_pycode(val: str):
    val = val.strip()
    if not val.startswith("${{"):
        return False
    if not val.endswith("}}"):
        return False
    tmp_val = val.replace("${{", "", 1).replace("}}", "")
    try:
        eval(tmp_val)
    except Exception as e:
        log.info(str(e))
        return False
    return True


def remove_tab(val: str):
    line_list = val.split(os.linesep)
    if line_list:
        first_line = line_list[0]
        tab_count = 0
        for word in first_line:
            if word != " ":
                break
            tab_count += 1
        for line_index, line in enumerate(line_list):
            line_list[line_index] = line.replace(" " * tab_count, "", 1)
        val = os.linesep.join(line_list)
    return val


def eval_python(val: str):
    import src.core.interpreter.executor
    # result = {
    #     # 代码
    #     'code': py_code,
    #     # 合法性校验
    #     'legality': validate_code(py_code),
    #     # 代码执行
    #     'result': exec_code(py_code)
    # }
    val = val.strip()
    val = val.lstrip("${{")
    val = val.rstrip("}}")
    result = src.core.interpreter.executor.call(val.strip())

    if result["legality"]:
        return result.get("result")
    else:
        raise Exception("pycode parse failed, {}".format(val))


def split_sub(k):
    pattern = r"\d+\.\d+"
    # 适配glibc: subpackage.glibc-compat-2.17.*
    if re.search(pattern, k):
        pattern = r"(\w+)\.(.*\d+)\.(.*$)"
        match = re.match(pattern, k)
        if match:
            return match.groups()
    return k.split(".", 2)


def format_subpackage(k, v, format_json, raw_json):
    if ":rpmWhen" in k:
        return
    if len(k.split(".")) < 3:
        return
    subpackage, name, key = split_sub(k)
    rpm_when_name = "{}.{}:rpmWhen".format(subpackage, name)
    rpm_when_key = "{}.{}.{}:rpmWhen".format(subpackage, name, key)
    if raw_json.get(rpm_when_key):
        key = "{} rpmWhen {}".format(key, raw_json.get(rpm_when_key))
    elif raw_json.get(rpm_when_name):
        name = "{} rpmWhen {}".format(name, raw_json.get(rpm_when_name))

    subpackage_name = subpackage + "." + name

    if ".runtimePhase." in k:
        v = remove_tab(v)
    if " rpmWhen " in key and "files" in key:
        tmp_key = key.split(" rpmWhen ")[0].strip()
        subpackage_name += key.replace(tmp_key, "")
    if key.startswith("meta."):
        meta, m_key = key.split(".", 1)
        format_json.setdefault(subpackage_name, {}).\
            setdefault(meta, {}).\
            setdefault(m_key, v)
    else:
        format_json.setdefault(subpackage_name, {}).\
            setdefault(key, v)


def format_patchset(k, v, format_json, raw_json):
    patchset, key = k.split(".", 1)
    format_json.setdefault(patchset, {}) \
        .setdefault(key, v)


def format_source(k, v, format_json, raw_json):
    source, key = k.split(".", 1)
    format_json.setdefault(source, {}) \
        .setdefault(key, v)


def format_rpm_global(k, v, format_json, raw_json):
    if "." not in k:
        return
    rpm_global, key = k.split(".", 1)
    format_json.setdefault(rpm_global, {}) \
        .setdefault(key, v)


def format_define_flags(k, v, format_json, raw_json):
    if "." not in k:
        return
    if isinstance(v, dict):
        compile_name = ""
        option = ""
        for param, val in v.items():
            if re.fullmatch("configure\w*\.(options|vars)", param):
                compile_name = param.split(".")[0]
                option = val
                break
        if not compile_name:
            log.error("error customization: {0}".format(k))
            return
        condition = v.get("when", "")
        default = v.get("default", "")
        build_requires = v.get("buildRequires", "")
        if build_requires != "" and default is True:
            for build_require in build_requires.split():
                if "buildRequires" in format_json and build_require not in format_json["buildRequires"] or \
                        "buildRequires" not in format_json:
                    format_json.setdefault('buildRequires', []).append(build_require)
        if "options" in param and "=" in val:
            option, default = val.split("=", 1)
        if condition:
            option += " when " + condition
        format_json.setdefault(f'build.{compile_name}.flags', {}).setdefault(option, default)
        return
    define_flags, key = k.split(".", 1)
    format_json.setdefault(define_flags, {}) \
        .setdefault(key, v)


def format_rpm_macros(k, v, format_json, raw_json):
    if "." not in k:
        format_json.setdefault(k, v)
        return
    source, key = k.split(".", 1)
    format_json.setdefault(source, {}) \
        .setdefault(key, v)


def format_phase(k, v, format_json, raw_json):
    v = remove_tab(v)
    format_json.setdefault(k, v)


def format_meta(k, v, format_json, raw_json):
    meta, key = k.split(".", 1)
    format_json.setdefault(meta, {}) \
        .setdefault(key, v)


def format_compile_flags(k, v, format_json, raw_json):
    if "build." not in k:
        return
    if ".flags." in k:
        build, key = k.split(".flags.", 1)
        format_json.setdefault(f'{build}.flags', {}).setdefault(key, v)
    elif re.match("build\." + ("|".join(list(CONFIG_SET_FILES.keys()))), k):
        from src.core.config_space import config_space
        key = k.split(".")[-1]
        config_key_name = k.split(".")[1]
        format_json.setdefault(config_key_name, {"ARCH": ARCH_SYS.get(config_space.arch, config_space.arch)}) \
            .setdefault(key, v)
    elif re.match("build\.(" + ("|".join(list(BASE_FLAGS_CANTACT.keys()))) + ")", k):
        key = k.split(".")[-1]
        format_json.setdefault("rpmGlobal", {}).setdefault(BASE_FLAGS_CANTACT.get(key, key), "%{?" + BASE_FLAGS_CANTACT.get(key, key) + "} " + v)
    elif re.match("build\.(" + ("|".join(list(BASE_FLAGS_REPLACE.keys()))) + ")", k):
        key = k.split(".")[-1]
        format_json.setdefault("rpmGlobal", {}).setdefault(BASE_FLAGS_REPLACE.get(key, key),  v )


def format_top(k, v, format_json, raw_json):
    if k.startswith("top."):
        k = k.replace("top.", "")
        if "defineFlags." in k:
            if not isinstance(v, dict):
                format_json.setdefault(k, v)
                return
            compile_name = ""
            option = ""
            for param, val in v.items():
                if re.fullmatch("(configure|cmake|make)\w*\.(options|vars)", param):
                    compile_name = param.split(".")[0]
                    option = val
                    break
            if not compile_name:
                log.error("error customization: {0}".format(k))
                return
            condition = v.get("when", "")
            default = v.get("default", "")
            if "options" in param and "=" in val:
                option, default = val.split("=", 1)
            if condition:
                option += " when " + condition
            format_json.setdefault(f'build.{compile_name}.flags', {}).setdefault(option, default)
        else:
            format_json.setdefault(k, v)


format_funcs = {
    "subpackage": format_subpackage,
    "patchset": format_patchset,
    "source": format_source,
    "rpmGlobal": format_rpm_global,
    "defineFlags": format_define_flags,
    "rpmMacros": format_rpm_macros,
    "phase": format_phase,
    "runtimePhase": format_phase,
    "meta": format_meta,
    "build": format_compile_flags,
    "top": format_top,
}


def format_package_json(package_json):
    # for handle subpackage, patchset, source
    format_json = {}
    filter = ["env.configureFlags"]
    for k, v in package_json.items():
        if k in filter:
            continue
        first_key = k.split(".", 1)[0]
        if " rpmWhen " in first_key:
            first_key = first_key.split("rpmWhen")[0].strip()
        func = format_funcs.get(first_key)
        if func is None:
            format_json[k] = v
            continue
        func(k, v, format_json, package_json)
    return format_json
