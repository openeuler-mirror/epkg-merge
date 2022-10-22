#!/usr/bin/python3
from src.core.interpreter import scanner
from src.core.interpreter import importer
from src.core.interpreter import illegal_import_exception
from src import log


default_lib = importer.import_default_lib()
for lib in default_lib:
    exec('import ' + lib)


class StartUp:

    @staticmethod
    def startup(config_space) -> dict:
        try:
            from src.core.config_space import config_space
            py_list = config_space.get('libs')
            scanner.scan_module(py_list)
            # If any code involves high-risk import, the startup fails
            scanner.scan_risk_import(py_list)
            # Import required for preloading code
            from src.core.interpreter import executor
        except illegal_import_exception.IllegalImportException as e:
            return {'startup_status': False, 'error_info': e.error_info}
        except Exception as e:
            return {'startup_status': False, 'error_info': e}
        else:
            return {'startup_status': True, 'error_info': None}
