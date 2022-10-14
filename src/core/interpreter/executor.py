#!/usr/bin/python3
import ast
from src.core.interpreter import constants
import sys
import os
import re


import_py = constants.import_py
from_import_list = constants.from_import_list
# 导入from import
for i in from_import_list:
    exec(i)
# 导入import的文件
for j in import_py:
    py_name = []
    py_path = []
    # 解析Linux路径
    if sys.platform == 'linux':
        py_name = re.findall(r'(\w+)+\.', j)
        py_path = re.findall(r'^/.*/', j)
    # 解析windows路径
    else:
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
    except Exception as e:
        result = e
        return result
    else:
        return result


def validate_code(py_code) -> bool:
    try:
        ast.parse(py_code.strip())
    except SyntaxError as e:
        print('Input isnt code.' + e)
        return False
    print('Code is ok.')
    return True
