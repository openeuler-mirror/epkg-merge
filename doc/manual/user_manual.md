## 用户使用说明书

工具为支持用户侧定制软件包配置文件组合、合并、转换工具。OS定制体现为，含代码逻辑的大量YAML文件及python函数库，按一定策略进行数据合并、变换、求值，输出为一组软件包的YAML，映射为具体包格式。

### 快速使用指导

#### 环境准备

- 操作系统：推荐使用linux
- python 3.8及以上

#### 编写或下载层模型

在使用分层定制工具前，需要先准备构建元数据。样例数据可以在下方链接中下载到

```
https://gitee.com/openeuler-customization/merge-package-configs/tree/master/tests/demo
```

#### 安装分层构建工具和转换工具

```bash
# 下载merge_configs-0.0.2-py3-none-any.whl  openEulerTransition-0.0.1-py3-none-any.whl
https://gitee.com/openeuler-customization/merge-package-configs/blob/master/dist/merge_configs-0.0.2-py3-none-any.whl
https://gitee.com/openeuler-customization/adapter-transition/blob/master/dist/openEulerTransition-0.0.1-py3-none-any.whl
# 安装whl
pip install merge_configs-0.0.2-py3-none-any.whl
pip install openEulerTransition-0.0.1-py3-none-any.whl
```

#### 执行分层定制工具

假设上面下载demo后，本地保存的路径为xxx，如果此时想到处软件包python的构建脚本，可以执行命令：

```
merge-configs -c xxx/config.yaml -p python3
```

执行完上面的命令之后，会在当前路径下生成合并之后的python3.yaml文件 和 python3.spec文件。

通过`merge-configs -h`命令，能够查看相关帮助

```
usage: merge-configs [-h] [-c CONFIG_FILE] [-p PACKAGES] [-o OUTPUT] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        the configuration file to be parsed
  -p PACKAGES, --packages PACKAGES
                        the parsed packages， use -p 'A B' to specify multiple packages
  -o OUTPUT, --output OUTPUT
                        which dir the output is redirected to
  -d, --debug           output the run log to the terminal
```



### 层模型介绍

```bash
├─layer2             # 层
│  └─pkgs            # 层中的软件包
│  │   └─python3    
│  │   └─index.yaml  # 层配置文件
├─layer_os
│  ├─pkgs
│  │  ├─...
│  │  ├─bash
│  │  │  └─bash.yaml        # 软件包元数据
│  │  │  └─files.yaml       # 软件包files打包文件
│  │  │  └─changelog.md     # 修改历史
│  │  │  └─phase.sh         # 构建脚本
│  │  │  └─runtimePhase.sh  # 构建脚本
│  │  ├─bind
│  │  ├─...
│  │  └─index.yaml  
│  └─types
│  │  └─pacakge.yaml  # 基础类型文件
└─layer_tools
│   ├─pkgs
│   │  ├─busybox
│   │  └─less
│   │  └─index.yaml  
│   └─use             # 全局定制选项
└─config.yaml         # 层配置
```

#### config.yaml文件内容说明

config.yaml为加载层模型的入口文件，内容包含了要加载的层目录名称；工具会编译当前目录下指定的层目录，后续可以使用绝对路径；

```yaml
layers:
    - layer_os
    - layer2
    - layer_tools
```

#### layer层模型

layer层模型主要内容包括：

- pkgs 软件包目录，其中每个软件包建立自己的文件夹
- types 给出了全局层模型的定义，定义了各个关键字的类型，合并方法，检验方法；（此处是基础定义，每个包中可以定义自身的合并策略或校验方法)
- use 全局参数，软件包可以引用全局参数，引用后全局的参数会加载到软件包的配置中（当前还没找到使用方式）
- lib python类库，这些py为全局使用，因此应当避免出现重复的函数名称

### 语法

#### 变量

##### 基础变量

基础变量为yaml的基本语法，`变量名: 变量值`；注意，yaml的语法中冒号与变量值之间，必须有一个空格；

```yaml
name: less
patchset:
  '0': less-394-time.patch
  '1': less-475-fsync.patch
```

##### 引用当前包中的变量

在配置中，如果想引用当前软件包的某个配置，可以使用 %%{变量名}来进行引用，例如：

```yaml
epol: 1
release: r%%{epol}
```

那么当通过分成定制工具处理之后，上面的内容会变成

```yaml
epol: 1
release: r1
```

##### 全局变量引用

如果软件包想引用其他软件包的值，需要使用全局引用的方式%%%{pkgs.xxx.yyy}, 例如：

```yaml
# bash.yaml
verison: 1.2.1

# python3.yaml
version: %%%{pkgs.bash.version}
```

那么当通过分成定制工具处理之后，上面的内容会变成

```yaml
# bash.yaml
verison: 1.2.1

# python3.yaml
version: 1.2.1
```

##### python语法

当需要使用python语句来求解某一个值时，可以使用{{ python语句 }}；建议此处的python语句尽量写的简单，如果内容需要比较复杂时候，建议将复杂内容放入lib之下

```python
# lib/a.py
def sum(a,b):
    return a+b
```

```yaml
epol: 1
release: 2
version: {{ sum( d.epol , d.release ) }} 
# python中引用当前包变量使用d.xxx，引用全局变量使用dd.xxx 对应上面的 %%xx %%%xxx
```

注意：上面的{{ 内容 }}，内容两边必须有空格分隔；

那么当通过分成定制工具处理之后，上面的内容会变成

```yaml
epol: 1
release: 2
version: 3
```

上述变量中的引用

```
局部引用：
   anywhere:  %%{key}
   in python: d.key

全局引用：
   anywhere:  %%%{key.path}
   in python: dd.key.path
```

#### 条件语法

##### 基于when实现的条件

条件语句写法为：`key when conditon`；举例：

```
patchset:
	0 when %%version<=1.3.0: xxxxx.patch
# 上面的条件表示当version<=1.3.0时，会打入xxxxx.patch；如果不满足条件则不合入
```

##### 运行时条件

当前的运行是条件，部分还是基于spec来使用的



### 使用方法

#### 基于spec生成yaml

软件包的一般性配置内容可以直接参考spec的写法，通常可以进行一一对应。可以使用上面的转换工具，将spec转为yaml的形式。

```
openEulerTransition -p xxx.spec
```



#### 在yaml中设置条件构建

在软件包的yaml中可以加入条件描述，如下面的内容；其表示sqlite默认为true，且如果sqlite为true时，会将enable内容加入到%configure中，开启对应的编译选项，并将buildRequires，files，subpackage.devel.files 的内容添加到对应的key当中。相反如果sqlite为false，那么不会进行添加并将 disable的内容加入到%configure中。

```yaml
# layer1/pkgs/xxx/xxx.yaml
useFlags:
    +sqlite:
        doc: sqlite3 loadable extension support
        enable: --enable-loadable-sqlite-extensions
        disable: --disable-loadable-sqlite-extensions
        buildRequires:
            - "sqlite-devel"
        files: |
          %{dynload_dir}/_sqlite3.%{SOABI_optimized}.so
          %dir %{pylibdir}/sqlite3/
          %dir %{pylibdir}/sqlite3/__pycache__/
          %{pylibdir}/sqlite3/*.py
          %{pylibdir}/sqlite3/__pycache__/*%{bytecode_suffixes}
        subpackage.devel.files: |
          %{pylibdir}/sqlite3/test
          %{dynload_dir}/_sqlite3.%{SOABI_debug}.so
```

如果要想指定开启或者关闭，可以在其他层中设置sqlite的值

```yaml
# layer2/pkgs/xxx/xxx.yaml
use.sqlite: true
```

上面将sqlite设置为true；（也可以设置为false）

#### 层的优先级

每一个配置文件需要包含一些属性，传递到所属各字段，以便确定它们在override层级中的位置。

- 第一优先级：origin package < update package

- 第二优先级：docType order

- 第三优先级：layerPrio 数字序

- 第四优先级：layerName 字典序

  


origin package 与 update package

```
一个YAML文件，可以定义一个软件包，也可以对另一个软件包做局部修改。
我们用如下两个概念加以区分：
- origin package file是一个软件包的原始定义。
- update package file是对（第三方）原始定义的补充与修改。
它们可以类比yocto里的bb与bbappend文件。

这里我们不采用bb/bbappend这样，以文件后缀名来区分origin/update，而是认为可以自动判断：
如果一个YAML包文件里定义了meta.xxx (spec:Summary/License/URL)这些字段，那么就认为它是origin package。
因为这些字段一旦定义，一般第三方没必要去修改。
```

docType 按优先级顺序从高到低定义如下：

```
   env-user
   env-project
   env-system
   build
   distro
   hw-machine
   hw-board
   hw-chip
   sw-package
   base
```

层的优先级docType 和layerPrio 设置，在pkgs/index.yaml中，此yaml的内容如下：

```yaml
configFilesPattern: (?P<_pkgname>[-0-9a-zA-Z]+)(/|\\)\1\.yaml
registerConfigSpaceForEachFile:
  pkgs.%%_basename:fspath: "%%_filepath"
  files."%%_filepath":
    name: "%%_basename" # can catch spell error if conflict with the name defined in yaml
    docType: base   # 设置层类型
    layerPrio: 9    # 层优先级
    includePhase: phase.sh
    includeRuntimePhase: runtimePhase.sh
    include: versions.yaml files.yaml
    :referAttrs: types.package
    meta:referAttrs: types.package.meta
    phase:referAttrs: types.package.phase
    runtimePhase:referAttrs: types.package.runtimePhase
```





### spec与yaml关键字对应关系

#### yaml字段统一使用camelCase命名风格

```
RPM spec fields mapping

	Name            =>  name
	Version         =>  version
	Release         =>  release
	Epoch		    =>  epoch

	Summary         =>  meta.summary
	Group		    =>  meta.group
	License         =>  meta.license 
	URL             =>  meta.homepage 
	%description    =>  meta.description  

	Source0         =>  source.0[:fetcher]
	Patch0          =>  patchset.0

	Provides        =>  provides
	Requires        =>  requires
	BuildRequires   =>  buildRequires
	Recommends      =>  recommends
	Suggests        =>  suggests
	Supplements     =>  supplements
	Enhances        =>  enhances
	Conflicts       =>  conflicts
	BuildConflicts  =>  buildConflicts
	Obsoletes       =>  obsoletes

	ExcludeArch     =>  excludeArch
	ExclusiveArch   =>  exclusiveArch
	BuildArch       =>  buildArch

	%package        =>  subpackage.<subname>

	%prep		    =>  phase.unpack + phase.patch
	%conf		    =>  phase.configure
	%build		    =>  phase.build
	%install	    =>  phase.install
	%check		    =>  phase.check

	%files		    =>  files
	%changelog	    =>  放入独立changelog.md文件

	%pre		    =>  runtimePhase.pre		
	%post		    =>  runtimePhase.post		
	%preun		    =>  runtimePhase.preun		
	%postun		    =>  runtimePhase.postun		
	%pretrans	    =>  runtimePhase.pretrans	
	%posttrans	    =>  runtimePhase.posttrans	
	%verify		    =>  runtimePhase.verify		
```
