#!/usr/bin/python3
from src.core.interpreter import constants
from src.core.interpreter import scanner
from src.log import log
import ast
import sys


import_py = constants.import_py
for j in import_py:
    py_name, py_path = scanner.path_resolution(j)
    sys.path.append(py_path[0])
    exec('from ' + py_name[0] + ' import *')


def call(py_code) -> dict:
    result = {
        'code': py_code,
        'legality': validate_code(py_code),
        'result': exec_code(py_code)
    }
    log.info(result)
    return result


def exec_code(py_code) -> str:
    try:
        result = eval(py_code)
    except Exception as e:
        result = e
        return py_code
    else:
        return result


def validate_code(py_code) -> bool:
    try:
        ast.parse(py_code.strip())
    except SyntaxError as e:
        log.error(e)
        return False
    log.info('Code is ok.')
    return True
