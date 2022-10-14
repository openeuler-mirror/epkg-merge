# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.


def is_pycode(val: str):
    val = val.strip()
    if not val.startswith("{{"):
        return False
    if not val.endswith("}}"):
        return False
    return True


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


def format_subpackage(k, v, format_json):
    subpackage, name, key = k.split(".", 2)
    format_json.setdefault(subpackage, {}).setdefault(name, {}) \
        .setdefault(key, v)


def format_patchset(k, v, format_json):
    patchset, key = k.split(".", 1)
    format_json.setdefault(patchset, {}) \
        .setdefault(key, v)


def format_source(k, v, format_json):
    source, key = k.split(".", 1)
    format_json.setdefault(source, {}) \
        .setdefault(key, v)


format_funcs = {
    "subpackage": format_subpackage,
    "patchset": format_patchset,
    "source": format_source
}


def format_package_json(package_json):
    # for handle subpackage, patchset, source
    format_json = {}
    for k, v in package_json.items():
        first_key = k.split(".", 1)[0]
        func = format_funcs.get(first_key)
        if func is None:
            format_json[k] = v
            continue
        func(k, v, format_json)
    return format_json
