#!/usr/bin/python3
from src.core.interpreter import scanner
from src.core.interpreter import importer
from src.core.interpreter import illegal_import_exception
from src.log import log


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
            startup_result = {
                'startup_status': False,
                'error_info': e.error_info
            }
            log.error(startup_result)
            return startup_result
        except Exception as e:
            startup_result = {
                'startup_status': False,
                'error_info': e
            }
            log.error(startup_result)
            return startup_result
        else:
            startup_result = {
                'startup_status': True,
                'error_info': None
            }
            log.info(startup_result)
            return startup_result
