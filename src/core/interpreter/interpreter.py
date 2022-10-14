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
            #     r'C:\Users\zhangshengjie\PycharmProjects\merge-package\merge-package-configs\tests\demo\layer\libs\calculate.py',
            #     r'C:\Users\zhangshengjie\PycharmProjects\merge-package\merge-package-configs\tests\demo\layer\libs\exclusive_info.py'
            # ]
            # 扫描方法名
            scanner.scan_module(py_list)
            # 扫描risk的import,并将白名单内的import加入constant中
            scanner.scan_risk_import(py_list)
            # # 加载executor中刚刚加入的import
            from src.core.interpreter import executor
        except Exception as e:
            return {'startup_status': e}
        else:
            return {'startup_status': True}


if __name__ == '__main__':
    # config_space = ConfigSpace()
    print(StartUp.startup(''))
    py_code = 'cal_sqrt(4)'
    from src.core.interpreter import executor
    print(executor.call(py_code))
