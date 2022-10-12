from enum import Enum

import_list = []
import_py = []


class DeafultLibs(Enum):
    math = 'math'
    datetime = 'datetime'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, DeafultLibs))


class DiskLibs(Enum):
    os = 'os'
    sys = 'sys'
    popen = 'popen'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, DiskLibs))

