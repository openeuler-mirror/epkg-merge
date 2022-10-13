#!/usr/bin/python3
from src.core.interpreter import scanner
from src.core.interpreter import importer
from src.core.interpreter import constants


# 导入常用库
default_lib = importer.import_default_lib()
for lib in default_lib:
    exec('import ' + lib)


class StartUp:
    # 启动

    @staticmethod
    def startup(config_space) -> dict:
        try:
            from src.core.config_space import config_space
            # 从ConfigSpace获取py文件
            py_list = config_space.get('libs')
            # py_list = [
            #     r'C:\Users\zhangshengjie\PycharmProjects\merge-package\merge-package-configs\tests\demo\layer\libs\calculate.py'
            # ]
            # 扫描方法名
            modulea_dict = scanner.scan_module(py_list)
            # 扫描risk的import
            imports_dict = scanner.scan_risk_import(py_list)
            for i in imports_dict:
                for j in i['import_lists']:
                    # 添加扫描到的第三方库
                    constants.import_list.append(j)
                # 添加扫描到的py文件
                constants.import_py.append(i['py_name'])
            # 加载executor中刚刚加入的import
            from src.core.interpreter import executor
        except Exception as e:
            return {'startup_status': e}
        else:
            return {'startup_status': True}


if __name__ == '__main__':
    # config_space = ConfigSpace()
    print(StartUp.startup(''))
    py_code = 'cal_floor(44)'
    from src.core.interpreter import executor
    print(executor.call(py_code))
