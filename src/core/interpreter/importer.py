#!/usr/bin/python3

from src.core.interpreter import constants


def import_default_lib() -> list:
    return constants.DeafultLibs.list()

def import_user_module() -> bool:
    pass
