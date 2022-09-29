# check模块设计
## 对外接口

check_value(key)

作用:
    对key对应的value进行校验
步骤:
    读取key的value
    获取key所在的类型，对应的checkFunc
    执行checkFunc，返回校验结果

input:
    key: 描述要合入的key信息，例如: pkgs.gcc.buildRequires
output:
    value: 返回校验结果

"""
def check_value(key):
    value = config-sapce.get(key)
    check_func = check_lib(key)  # 返回当前key的check_func
    check_result = check_func(value)   # 校验value
    return check_result

def check_lib(key):
    # 根据key的内容获取check_func
    pass
"""

## 与其他模块的交互
check_func 在定义在lib中，直接传递给解释器？