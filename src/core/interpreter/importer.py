#!/usr/bin/python3

from src.core.interpreter import constants


def import_default_lib() -> list:
    return constants.DeafultLibs.list()

