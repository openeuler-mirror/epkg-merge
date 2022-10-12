#!/usr/bin/python3
from constants import DiskLibs

# 扫描模块名
def scan_module(py_list) -> dict:
    list_modules = []
    for py in py_list:
        method_dict = {
            "py_name": py,
            "module_lists": get_methods_name(py)
        }
        # py_name = re.findall(r'(\w+)+\.', py)
        # py_path = re.findall(r'^.*\\', py)
        # sys.path.append(py_path[0])
        # exec('import ' + py_name[0])
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
    import_lists = []
    with open(py, encoding='utf-8') as f:
        line = f.readline()
        while line:
            if line.startswith("import "):
                import_i = line[7:].strip()
                # 过滤高危库
                for i in DiskLibs.list():
                    if import_i == i:
                        break
                else:
                    import_lists.append(import_i)  # 去除 "import"
            line = f.readline()
    return import_lists
