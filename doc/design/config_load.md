# 配置文件

## 入口配置文件

工具的入口配置文件，需要指定一组layers目录
最简形式如下

	main_config.yaml
		layers:
		- path1
		- path2
		- path3

LayerLoader 将遍历以上目录，递归加载其下的index.yaml到config_space，
完成config_space的初始骨架搭建，为惰性求值做好准备。

## layer目录结构

	layer.yaml

	lib/module1.py
	lib/module2.py

	pkgs1/index.yaml
	pkgs1/gcc/gcc.yaml
	pkgs1/llvm/llvm.yaml

	pkgs2/index.yaml
	pkgs2/bash/bash.yaml
	pkgs2/lftp/lftp.yaml

## index.yaml

index.yaml定义所在目录及递归子目录下
- 配置文件列表（正则表达式）
- 配置文件到配置空间的映射关系
- 批量添加字段key/val到下辖所有配置文件

index.yaml样例

	configFilesPattern: (?<_pkgname>[-0-9a-z]+)/\1\.yaml
	registerConfigSpaceForEachFile:
		# 建立key=>file mapping，用于延迟加载
		pkgs.%%_basename.fspath: %%_filepath

		# 定义适用于本组文件的公共字段/属性
		files."%%_filepath".include:
			name: %%_basename # can catch spell error if conflict with the name defined in yaml
			includePhase: phase.sh
			includeRuntimePhase: runtimePhase.sh
			include: versions.yaml files.yaml
			:referAttrs: types.package
			meta:referAttrs: types.package.meta
			phase:referAttrs: types.package.phase
			runtimePhase:referAttrs: types.package.runtimePhase

其中的%%宏引用，需要LayerLoader/YAMLLoader支持下面的隐含字段

	_filepath: /full/path/to/pkgname/pkgname.yaml
	_dirname:  /full/path/to/pkgname
	_filename: pkgname.yaml
	_basename: pkgname

这些字段可供配置文件引用，LayerLoader/YAMLLoader负责把它们替换为实际值。

## YAMLLoader 加载要点

1) filesystem path => config space path

如果直接加载YAML，那么读取YAML中的`cspath`字段，以便将YAML其它字段加载到指定的配置空间路径
如果延迟加载YAML，那么收到参数`fspath`及`cspath`，将`fspath`所在的YAML内容加载到`cspath`指定路径

2) 合入YAML文档include字段指向的附属配置文件


4) 对YAML字段:
- 替换key中的%%宏
- 如有:checkFunc属性，执行检查函数
- 如有:transformFunc属性，执行变换函数以引入额外字段
- value 原封不动加入 :values 属性，同时加入相关信息

	key:values +=
			{
				value: %%key
				origin: %%fspath
				when: when_cond
			}

5) 新加载的字段及字段属性，自动添加到相应 :loadedKeys :loadedAttrs 备查

6) 在配置空间注册文件信息，以便merge时取用

	files."%%fspath".cspath:
	files."%%fspath".docType:
	files."%%fspath".layerName:
	files."%%fspath".layerPrio:

## config file <<==>> config space 模型

config space 是核心内存数据模型。
config files 是核心磁盘数据模型。

config files index是索引数据库，包含所有config files的信息
映射信息：
	config space path 1:N==> config files
该映射信息用于支撑按需加载/惰性求值/cache复用等关健特性。

映射的建立方式：
1) 单个 full config file 包含字段
	cspath: pkgs.bash
2) 一组 full config files 按特定方式组织目录结构/文件名，
然后用一个index.yaml文件来统一描述文件系统路径到配置空间路径的映射规则。
最好是不加修改的一对一映射，文件路径直接代表配置路径，方便理解和记忆。

样例1：

	yaml file
		cspath: a.b
		c: yyy
=>
	config space
		a.b.c: yyy

样例2：
	user yaml
		cspath: pkgs
		bash.version: v1
		gcc.version: v2
=>
	config space
		pkgs.bash.version: v1
		pkgs.gcc.version: v2

通常不直接在一个个yaml里写`cspath`，而是在index.yaml里对一组文件定义`cspath<=>fspath`双向映射。

## phase.sh for build phases

shell脚本字段，可写到独立的.sh文件中去.

举例
	YAML
	phase.postInstall:
	  # remove la file
	  find %{buildroot} -name '*.la' -exec rm -f {} ';'
<=>
	phase.sh

	postInstall() {
	  # remove la file
	  find %{buildroot} -name '*.la' -exec rm -f {} ';'
	}

加载phase.sh到config space的过程:
 
LayerLoader根据index.yaml的以下内容，自动添加

		includePhase: phase.sh

RPM spec的build scriptlets都是shell script，这一般都够用好用。
如果未来某些本来就依赖python的项目真的需要用python, 可以类似的

		includePhase: phase.py

然后增强transform_include_phase，支持python函数加载。

## build phases 函数拆分定制

支持把复杂的build phase拆分为小函数。以便更好的模块化，并方便定制各函数。

以phase.build为例，拆分方法：
- 允许定义``phase.build_xxx/yyy``等函数，特点是以``build_``为前缀。
- phase.build定义为
	build_xxx
	build_yyy
- 转为spec时，在%build小节自动加入``phase.build_*``函数定义

	%build

	# from phase.build_*
	function build_xxx()
	{
		...
	}

	function build_yyy()
	{
		...
	}

	# from phase.build
	build_xxx
	build_yyy

## runtimePhase.sh for runtime scriptlets

以下spec字段可存到独立的runtimePhase.sh
体现为脚本中的一个个函数。

	https://rpm-software-management.github.io/rpm/manual/spec.html
	Runtime scriptlets
	Basic scriptlets

	    %pre
	    %post
	    %preun
	    %postun
	    %pretrans
	    %posttrans
	    %verify

	Triggers

	    %triggerprein
	    %triggerin
	    %triggerun
	    %triggerpostun

	More information is available in trigger chapter.
	File triggers (since rpm >= 4.13)

	    %filetriggerin
	    %filetriggerun
	    %filetriggerpostun
	    %transfiletriggerin
	    %transfiletriggerun
	    %transfiletriggerpostun

加载到YAML，形式如下

	runtimePhase:transformFunc: transform_include_runtime_phase
	runtimePhase:
		pre:
		post:
		...

### 加载 lua scriptlets

先看一个lua样例：

Spec:
	%post –p <lua>
	xxx

	%posttrans -e –p <lua>
	yyy

YAML:
	runtimePhase:
		post:rpm_macro_param: -p <lua>
		post: |
			xxx
		posttrans:rpm_macro_param: -e -p <lua>
		posttrans: |
			yyy

runtimePhase.lua:

	function post()
		--:rpm_macro_param: -p <lua>
		xxx

	function posttrans()
		--:rpm_macro_param: -e -p <lua>
		yyy

注意到每个scriptlet可以分别指定语言选项，所以需要定义两个一般化的转换规则：

规则1 spec <> YAML
spec里的 rpm macro参数，映射为YAML字段的一个`:rpm_macro_param`属性

规则2 YAML <> 分立文件
YAML里的字段属性

	attr: val

在转为分立文件时，自动转换为注释后的文本行

	--:attr: val (lua)
	#:attr: val  (shell, %files)

phase/runtimePhase/files等很多宏参数，都可以按照以上规则统一转换。

为了支持多语言，includePhase/includeRuntimePhase应当定义为

	includePhase: phase.sh phase.lua
	includeRuntimePhase: runtimePhase.sh runtimePhase.lua

它们应当接受一组文件路径，然后依次搜索加载所有文件。

### 缩进问题

spec里的scriptlets没有缩进。转换为.sh后自动缩进会比较好看，但是有几种情况下存在困难：
- here document (EOF)
- multi-line string

### %if 问题

scriptlets内部或者外部，都可能有%if/%endif条件。这些使得.sh看起来不是一个合法的shell脚本。
一种办法是自动替换为加注释的"### %if/%endif"，但仍然可能存在非法情况。所以还是保持原样好。

未来的scriptlets条件语句，尽量用when条件定义。如

	%if %{shared}
	GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -buildmode=shared -v -x std
	%endif

	%if %{race}
	GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -race -v -x std
	%endif

=>

	phase.postBuild when +shared: GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -buildmode=shared -v -x std
	phase.postBuild when +race:   GOROOT=$(pwd) PATH=$(pwd)/bin:$PATH go install -race -v -x std

把when条件较为自然的编码在.sh?

方案1
以下实验在bash下通过，但ash, dash, busybox sh都不支持。
鉴于这些都是中间形式，最终在构建环境中，不再有这些when条件，所以算不上是硬伤。
不过它不完备，难以编码较复杂的OR条件组合。简单的AND组合可以通过多个?表达。

	$ build?+xxx() { echo ; }
	$ build?-xxx() { echo ; }
	$ build?xxx=yyy() { echo ; }
	$ build?%%xxx!=y() { echo ; }
	$ build?arch=a,b,c() { echo ; }
	$ build?@1.1:1.2() { echo ; }

方案2

	## when cond1
	build() { echo ; }

	## when cond2
	build() { echo ; }

## 独立myfun.py文件

当一个YAML需要大量定义python逻辑时，可抽取为独立myfun.py文件
在YAML里这样加载

	includeLib:transformFunc: transform_include_lib
	includeLib: myfun.py

transform_include_lib 将其中的函数加载到 lib.myfun 字段下，供本YAML内置python code调用。
这样定义的局部库函数，在求值时需要连同调用它的python code一起，传给python interpreter server。
服务端需要检察，确保它们不与全局库函数同名。

## include 字段

方便定义包的多版本、多变体
允许同时安装多版本。

例子：
	gcc-10.yaml
		include: gcc.yaml
		version: 10

include还可用于合入工具自动生成的JSON文件，如对应包的versions.json

## 全局注册 自动include

每个文件说明自己的全局路径
别人引用时可自动加载

还可以由一个映射文件来描述配置空间路径与文件路径的映射关系

## per-field溯源能力

最终package文件的各自段来自哪个原始文件字段，需要保有记录。
呈现给用户，方便调试和理解。
JSON + debuginfo k/v

## on-demand file loading

为了可以scale to十万软件包。
多数的日常运行，只涉及rebuild一个较小的变动子集，应当使工作量可控。

## caching

避免重复执行
- package.yaml 合并、解析
- package 构建

## YAML limitation

### expression start with string

This is invalid:

        key!: "hi" if True else "aa"

This is valid:

        key!: |
                "hi" if True else "aa"

### version number

This should be string, but it's intepreted as float number:

        version: 1.0

correct form:

        version: "1.0"

Or use strictyaml (https://hitchdev.com/strictyaml/why/implicit-typing-removed/)
