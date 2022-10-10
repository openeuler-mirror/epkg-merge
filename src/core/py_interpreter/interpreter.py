#!/usr/bin/python3
import contextlib
import sys

from collecter import collect_py
from scanner import scan_module, scan_risk_import
from importer import import_user_module, import_default_lib
from executor import validate_code
from io import StringIO

# 导入常用库
default_lib = import_default_lib()
for lib in default_lib:
    exec('import ' + lib)
# 导入ConfigSpace获取的所有python模块
import_user_module()


# 启动
def startup(config_space) -> dict:
    # 从ConfigSpace获取py文件
    py_list = collect_py(config_space)
    # 扫描模块名
    scan_module(py_list)
    # 扫描risk的import
    scan_risk_import(py_list)


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


def exec_code(py_code):
    with stdoutIO() as s:
        try:
            exec(py_code)
        except:
            return False
    return s.getvalue()


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


if __name__ == '__main__':
    py_list = [
        ''
    ]
    startup(1)
    py_code = 'print(math.sqrt(4))'
    print(call(py_code))
