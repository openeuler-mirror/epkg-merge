from enum import Enum

# Deafult_Libs = Enum(
#     "time",
#     "datetime",
#     "random",
#     "math"
# )

class DeafultLibs(Enum):
    math = 'math'
    datetime = 'datetime'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, DeafultLibs))

