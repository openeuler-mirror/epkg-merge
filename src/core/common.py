# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.
import os


def is_pycode(val: str):
    val = val.strip()
    if not val.startswith("{{"):
        return False
    if not val.endswith("}}"):
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
    val = val.lstrip("{{")
    val = val.rstrip("}}")
    result = src.core.interpreter.executor.call(val.strip())

    if result["legality"]:
        return result.get("result")
    else:
        raise Exception("pycode parse failed, {}".format(val))


def format_subpackage(k, v, format_json, raw_json):
    if ":rpmWhen" in k:
        return
    if len(k.split(".")) < 3:
        return
    subpackage, name, key = k.split(".", 2)
    rpm_when_name = "{}.{}:rpmWhen".format(subpackage, name)
    if raw_json.get(rpm_when_name):
        name = "{} rpmWhen {}".format(name, raw_json.get(rpm_when_name))

    rpm_when_key = "{}.{}.{}:rpmWhen".format(subpackage, name, key)
    if raw_json.get(rpm_when_key):
        key = "{} rpmWhen {}".format(key, raw_json.get(rpm_when_key))

    subpackage_name = subpackage + "." + name

    if ".runtimePhase." in k:
        v = remove_tab(v)
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
}


def format_package_json(package_json):
    # for handle subpackage, patchset, source
    format_json = {}
    filter = ["env.configureFlags"]
    for k, v in package_json.items():
        if k in filter:
            continue
        first_key = k.split(".", 1)[0]
        func = format_funcs.get(first_key)
        if func is None:
            format_json[k] = v
            continue
        func(k, v, format_json, package_json)
    return format_json
