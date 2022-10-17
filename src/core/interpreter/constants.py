from enum import Enum


import_py = []
from_import_list = []
white_list_libs = ['math', 'datetime']


class DeafultLibs(Enum):
    math = 'math'
    datetime = 'datetime'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, DeafultLibs))


