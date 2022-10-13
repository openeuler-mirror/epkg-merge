#!/usr/bin/python3
import ast
from src.core.interpreter import constants
import sys
import re


import_list = constants.import_list
import_py = constants.import_py
for i in import_list:
    exec('import ' + i)
for j in import_py:
    py_name = re.findall(r'(\w+)+\.', j)
    py_path = re.findall(r'^.*\\', j)
    sys.path.append(py_path[0])
    exec('from ' + py_name[0] + ' import *')


# 执行
def call(py_code) -> dict:
    result = {
        # 代码
        'code': py_code,
        # 合法性校验
        'legality': validate_code(py_code),
        # 代码执行
        'result': exec_code(py_code)
    }
    return result


def exec_code(py_code) -> str:
    result = 'Code execution error'
    try:
        result = eval(py_code)
    except:
        return result
    else:
        return result


def validate_code(py_code) -> bool:
    try:
        ast.parse(py_code.strip())
    except SyntaxError:
        print('Input isnt code.')
        return False
    print('Code is ok.')
    return True
