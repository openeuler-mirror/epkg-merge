#!/usr/bin/python3
import contextlib
import sys

from src.core.interpreter.scanner import scan_module, scan_risk_import
from src.core.interpreter.importer import import_user_module, import_default_lib
from src.core.interpreter.executor import validate_code
from io import StringIO
from src.core.interpreter.collecter import collect_py

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
    # py_list = [
    #     r'C:\Users\zhangshengjie\PycharmProjects\merge-package\merge-package-configs\tests\demo\layer\libs\calculate.py',
    #     r'C:\Users\zhangshengjie\PycharmProjects\merge-package\merge-package-configs\tests\demo\layer\libs\exclusive_info.py',
    #     r'C:\Users\zhangshengjie\PycharmProjects\merge-package\merge-package-configs\tests\demo\layer\libs\restart.py'
    # ]
    # 扫描模块名
    # modulea_dict = scan_module(py_list)
    # # 扫描risk的import
    # imports_dict = scan_risk_import(py_list)
    # for i in imports_dict:
    #     for j in i['import_lists']:
    #         exec('import ' + j)


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
    result = 1
    with stdoutIO() as s:
        try:
             result = eval(py_code)
        except:
            return result
    # return s.getvalue()
    return result


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


if __name__ == '__main__':
    # startup(1)
    py_code = 'not False'
    print(call(py_code))
