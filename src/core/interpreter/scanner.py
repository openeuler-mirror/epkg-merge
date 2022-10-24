#!/usr/bin/python3
import os
import re
import sys

from src.core.interpreter import constants
from src.core.interpreter import illegal_import_exception
from src.log import log


def scan_module(py_list) -> dict:
    list_modules = []
    for py in py_list:
        method_dict = {
            "py_name": py,
            "method_lists": get_methods_name(py)
        }
        list_modules.append(method_dict)
        log.info(method_dict)
    return list_modules


def scan_risk_import(py_list) -> dict:
    list_imports = []
    for py in py_list:
        imprt_lists = get_import_name(py)
        import_dict = {
            "py_name": py,
            "import_lists": imprt_lists
        }
        list_imports.append(import_dict)
        log.info(import_dict)
    return list_imports


def get_methods_name(py):
    method_lists = []
    method_lists_noparam = []
    with open(py, encoding='utf-8') as f:
        line = f.readline()
        while line:
            if "def " in line:
                k1, v1 = line.split(':', 1)  
                func_i = k1[4:]
                method_lists.append(func_i)  
                klist = func_i.split("(")  
                k2 = klist[0]
                method_lists_noparam.append(k2)
            line = f.readline()
    return method_lists


def get_import_name(py):
    py_name, py_path = path_resolution(py)
    scan_files = scan_dir(py_path[0])
    for k in scan_files:
        scan_file, scan_file_path = path_resolution(k)
        constants.white_list_libs.append(scan_file[0])
    constants.import_py.append(py)
    import_lists = []
    with open(py, encoding='utf-8') as f:
        line = f.readline()
        line = line.lstrip()
        while line:
            if line.startswith('import ') | line.startswith('from '):
                is_white_list = False
                for i in constants.white_list_libs:
                    if i in line:
                        import_lists.append(line)
                        is_white_list = True
                        break
                if not is_white_list:
                    raise illegal_import_exception.IllegalImportException('File contains illegal import : ' + line)
            line = f.readline()
    return import_lists


def scan_dir(file_path):
    file_list = []
    for curDir, dirs, files in os.walk(file_path, topdown=False):
        for file in files:
            if file.endswith('.py'):
                file_list.append(file)
    return file_list


def path_resolution(py):
    if sys.platform == 'linux':
        py_name = re.findall(r'(\w+)+\.', py)
        py_path = re.findall(r'^/.*/', py)
    else:
        py_name = re.findall(r'(\w+)+\.', py)
        py_path = re.findall(r'^.*\\', py)
    return py_name, py_path
