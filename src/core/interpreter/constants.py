from enum import Enum

# 导入的pylist
import_py = []
# 白名单
white_list_libs = ['math', 'datetime']


class DeafultLibs(Enum):
    math = 'math'
    datetime = 'datetime'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, DeafultLibs))


