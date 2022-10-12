#!/usr/bin/python3

from src.core.interpreter.constants import DeafultLibs


def import_default_lib() -> list:
    return DeafultLibs.list()

def import_user_module() -> bool:
    pass
