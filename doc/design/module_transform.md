# transform模块设计
## 模块说明
    transform模块下的函数，输入为字段值，输出为一个hash object。
    调用方会把hash object转为key/val，供YAMLLoader插入config-space。
## 对外接口
    transform_include_phase(val)
    transform_include_runtime_phase(val)
    transform_include_lib(val)
    transform_use_configure_flags(val)
    transform_iuse_flags(val)

## transform_include_phase, transform_include_runtime_phase, transform_include_lib
作用:
    解析传入的文件，并将shell文件解析后，获取其中的函数名和函数体，保存为hash对象返回
    transform_include_runtime_phase, transform_include_lib 
    与 transform_include_phase 共享底层实现代码，只是加载的目标字段不同。
步骤:
    1、读取shell文件
    2、解析shell文件获取函数名及函数体
    3、创建hash对象，将函数名作为key,函数体作为value
    4、返回hash对象

input:
    val: shell文件的绝对路径，例如: "/c/x/phase.sh"
output:
    value: 返回shell解析后的hash对象

"""
def transform_include_phase(val):
    read shell script file
    hash = {}
    for each shell function:
        hash[func_name] = func_code
    return hash
"""

## transform_use_configure_flags

作用:
    解析传入的字符串，并将字符串的内容
步骤:
    如何直接写成hash，这个函数就不用调用了!

input:
    val: 字符串
output:
    value: hash

"""
def	transform_use_configure_flags(val)
    for each feature, output key/vals:
        use.f1:type: bool
        use.f1:default: true/false if f1 starts_with +/-
        use.f1:doc: this is some xxx feature
        env.configureFlags when +f1: --with-f1
        env.configureFlags when -f1: --without-f1
        buildRequires when +f1: build-deps-for-f1
        requires when +f1: runtime-deps-for-f1
        recommends when +f1: runtime-recommends-for-f1
        conflicts when +f1: conflicts-for-f1
"""

## transform_iuse_flags
作用:
    解析传入的字符串，并将字符串的内容，转换为hash，调用者写入config-space
步骤:
    1、读取用户输入的命令行字符串，并解析
    2、依次写入config-space

inpurt:
    val: 命令行字符  example: "+X +ssl test"
output:
    None

"""
def transform_iuse_flags(val):
    for each feature, output key/vals:
        inherit: use.feature
        use.feature:default: true/false if feature starts_with +/-

"""

## 与其他模块的交互
config_space.get(key)
expand_marcro(val)