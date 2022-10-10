
## 模块设计
##### 启动序列图：
```sequence
工具入口->>startup: 启动python解释器
startup->>collector: 从ConfigSpace获取py文件
collector->>startup: 返回结果
startup->>scanner: 扫描模块名
scanner->>startup: 返回结果
startup->>importer: 扫描risk的import
importer->>startup: 返回结果
startup->>importer: 导入常用库
importer->>startup: 返回结果
startup->>importer: 导入ConfigSpace获取的所有python模块
importer->>startup: 返回结果
startup->>工具入口: 返回状态
```
##### 执行序列图：
```sequence
merge模块->>call: 传入待执行代码
call->>executor: 检查代码合法性
executor->>call: 返回结果
call->>executor: 执行代码
executor->>call: 返回结果
call->>merge模块: 返回执行结果
```
## 对外接口
##### 启动：
def startup -> result: dict

作用：
    1、启动python解释器模块，创建解释器对象(单例)
    2、从ConfigSpace获取所有py文件
    3、扫描py所有模块名，检查所有模块是否有名称冲突
    4、扫描py所有import项，检查是否有风险import
    5、import常用python库
    6、import从ConfigSpace获取的所有python模块
    7、返回启动状态,成功/失败

input:
    ConfigSpace: layerLoader模块加载的内存空间，里面包含本次加载的所有py文件

output:
    result: 启动状态 => {'result':'', 'description':''}

"""
##### 执行：

def call(py_code: str) -> result

作用：
    对python code代码解释执行，并返回执行结果

步骤：
    1、传入代码合法性校验（危险import检查）
    2、执行代码
    3、返回执行结果
input:
    pycode: 待执行的python code字符串，例如：math.sqrt(4)

output:
    result: 执行后的输出结果 => {'output':'', 'result':'', 'description':''}

"""







