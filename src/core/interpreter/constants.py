from enum import Enum


import_py = []
from_import_list = []


class DeafultLibs(Enum):
    math = 'math'
    datetime = 'datetime'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, DeafultLibs))


class WhiteListLibs(Enum):
    math = 'math'
    datetime = 'datetime'
    exclusive_info = 'exclusive_info'
    calculate = 'calculate'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, WhiteListLibs))

