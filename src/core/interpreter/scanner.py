#!/usr/bin/python3
import os
import re
import sys

from src.core.interpreter import constants
from src.core.interpreter import scanner


# 扫描模块名
def scan_module(py_list) -> dict:
    list_modules = []
    for py in py_list:
        method_dict = {
            "py_name": py,
            "module_lists": get_methods_name(py)
        }
        list_modules.append(method_dict)
    print("扫描的方法名：")
    print(list_modules)
    return list_modules

# 扫描risk的import
def scan_risk_import(py_list) -> dict:
    list_imports = []
    for py in py_list:
        import_dict = {
            "py_name": py,
            "import_lists": get_import_name(py)
        }
        list_imports.append(import_dict)
    print("扫描的模块名：")
    print(list_imports)
    return list_imports


def get_methods_name(py):
    func_lists = []
    func_lists_noparam = []
    with open(py, encoding='utf-8') as f:
        line = f.readline()
        while line:
            if "def " in line:
                k1, v1 = line.split(':', 1)  # 去除冒号之后的备注
                func_i = k1[4:]
                func_lists.append(func_i)  # 去除 "def"
                # 只读取函数，不包含参数
                klist = func_i.split("(")  # 防止函数的参数中有括号
                k2 = klist[0]
                func_lists_noparam.append(k2)
            line = f.readline()
    return func_lists

def get_import_name(py):
    # 扫描文件路径下所有文件，并加入白名单内
    py_name = []
    py_path = []
    # 解析Linux路径
    if sys.platform == 'linux':
        py_name = re.findall(r'(\w+)+\.', py)
        py_path = re.findall(r'^/.*/', py)
    # 解析windows路径
    else:
        py_name = re.findall(r'(\w+)+\.', py)
        py_path = re.findall(r'^.*\\', py)
    scan_files = scanner.scanDir(py_path[0])
    for k in scan_files:
        if sys.platform == 'linux':
            scan_file_no_suffix = re.findall(r'(\w+)+\.', k)
            constants.white_list_libs.append(scan_file_no_suffix[0])
        else:
            scan_file_no_suffix = re.findall(r'(\w+)+\.', k)
            constants.white_list_libs.append(scan_file_no_suffix[0])
    # 取得需要import的列表
    import_lists = []
    constants.import_py.append(py)
    with open(py, encoding='utf-8') as f:
        line = f.readline()
        while line:
            if line.startswith('import') | line.startswith('from '):
                # 白名单匹配
                for i in constants.white_list_libs:
                    if i in line:
                        constants.from_import_list.append(line)
                        import_lists.append(line)
                        break
            line = f.readline()
    return import_lists


def scanDir(file_path):
    # 获取该路径下的所有文件
    files = os.listdir(file_path)

    file_list = []

    # 遍历所有文件
    for file in files:
        # 把文件路径和文件名结合起来
        file_d = os.path.join(file_path, file)
        # 判断该文件是单个文件还是文件夹
        if os.path.isdir(file_d):  # 如果是文件夹则递归调用 scanDir() 函数
            scanDir(file_d)
        else:
            file_list.append(file)
    return file_list
