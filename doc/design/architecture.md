# 分层定制工具架构

支持用户侧定制、厂商overlay组合的包管理器之：
软件包配置文件组合、合并、转换工具
==================================

OS定制体现为，含代码逻辑的大量YAML文件及python函数库，
按一定策略进行数据合并、变换、求值，输出为一组数据JSON，映射为具体包格式。

## 设计目标

- 易理解、易定制、易调试、不易出错、多而不乱、可以scale
- 破旧立新导向：理想的包格式应该长什么样子。集各家所长，参考但不受限于当前流行包格式

## 样例

baseos/package1.yaml
	key1: val1
	key2: {{ python code on d.key1 }}

layer1/package1.yaml
	key1: val2

layer2/package1.yaml
	key2: {{ updated python code on d.key1 }}

after merging
	key1: val2
	key2: {{ updated python code on d.key1 }}

must be DAG, error on circle
	# key1 finalize后，对 key2 求值，得到确定性的json
	# 实际求值过程可以惰性、递归进行
	# python code表述了字段之间的逻辑关系
	JSON data keys relationship

after finalized

	KV set1: describe inputs
	KV set2: describe depend graph
	KV set3: pass as ENV to build scripts autotool class + pkg script

## 工作流程

input project/layer/package yaml files (with embedded python code)
    + library python files
=> composite
	include
	inherit
=> sanity checks
   => check_function1
   => check_function2
   => check_function3
=> data pipeline 
   => transform_function1 # add key2 based on key1
   => transform_function2
   => transform_function3
=> per-package-file aggregate/merge
   => merge_function1 # merge 2 layers for a field
   => merge_function2
   => merge_function3
=> embedded python code delayed evaluation
=>
output package files (JSON)
with extra info (for debug, cache, etc.)
=>
target package format (spec, nix, bb, etc.)

=> (后续步骤，不在本工具范围内)
build system

## 应用场景

可分上下两层实现，为每一层建一个独立的git repo:
L0: 一个通用的configs merge tool
L1: 一个软件包configs merge tool

长远来看，该工具的使用方式，可以是
- 独立运行
- 提供语言API，供python/javascript等脚本调用
- 被一些需要处理大量配置文件的项目集成使用
- 被source-based distro的包管理器集成使用，提供用户侧定制构建与安装配置能力

## 模块架构

rust module
+---RPC----python interpreter, runs python expressions/functions
+---RPC----javascript interpreter, runs javascript expressions/functions
+---FFI----python app
+---FFI----javascript app

## CLI invocation

Usage:

	merge-configs -c config_file -o output -d debug

project layout:

	# pure functions called by yaml python
	# auto import, detected by pattern
	# lib.module1.func1()
	lib/module1.py
	lib/module2.py
	lib/module3.py

	types/package.yaml
	types/path.yaml
	types/PATH.yaml

	use/<feature>.yaml

	pkgs/<build_system1>/index.yaml
	pkgs/<build_system1>/bash/bash.yaml
	pkgs/<build_system1>/lftp/lftp.yaml

entry config
	layers:
	- /path/to/layer1 # each has a unique name
	- /path/to/layer2
	- /path/to/layer3

## language API

https://pyo3.rs/v0.16.4/conversions/tables.html

	setup(layers_config)
预取一组keys
	prefetch(keys)

对象访问: 返回某一path层级下的所有kv，格式为JSON
	get_json(path)

标量访问: 返回某一key的值
	get_int(key)
	get_float(key)
	get_bool(key)
	get_datetime(key)
	get_string(key)

数组访问: 返回某一key的值
	get_string_array(key)

## Main module

input:
	config.yaml

		layers: # 最简形式，按需扩展格式
		- /path/to/layer1
		- /path/to/layer2
		- /path/to/layer3

action:
	for each layers
		call LayerLoader
	call PythonInterpreter(all layers)

## rust layers init module (LayerLoader)

input:
	layer dir
output:
	config_space
		files.*
		*.files
action:
	for each index.yaml in layer dir
		register all yaml files
		register all lib/xxx.py
		register layer info to layers.xxx

config file preload or delayed-load:

	if is global config that impacts many keys
		# preload
		call load module
	else
		# load on demand
		# create mapping: config file <=> key
		config_space[files.$fspath.cspath] = $cspath
		config_space[files.$fspath.layer] = layer
		config_space[$cspath.fspath] += $fspath

## rust config file loader module (YAMLLoader)

input:
	key
action:
	get  config files from config_space.$key.files
	load config files into config_space.$key.*
基本数据变换:
	load_configs(key):
		return if config_space.$key:loaded
		config_space.$key:loaded = true
		priority = compute_priority(layer, file)
		hash = load yaml/json/jsonnet/cue/sh file
		flatten hash into a.b.c format
		for each flattened leaf_key
			config_space.$key:loadedKeys += leaf_key
			config_space.$leaf_key:values += {value: val, origin: file, when: xxx}

YAMLLoader 最主要的结果就是加载各字段到 :values 属性
因为分层定制允许多个YAML对同一个key赋值，它们都会被记录在:values里。
同一个文件也可能对一个key多次赋值。比如

	gcc.yaml
		requires when +a: alib
		requires when +b: blib

YAMLLoader 会把它们加载为

		requires:values {
			value: alib, when: +a, origin: /full/path/to/gcc.yaml
			value: blib, when: +b, origin: /full/path/to/gcc.yaml
		}

当需要对requires字段求值时，这些:values将传给merge函数，做合并求值
当两个when都满足是，最终结果成为

		requires: alib, blib

## rust DAG module

核心数据结构：
	维护一个`leaf_key`的DAG hash

		key1: %%{key2} or %%%{key2}
	=>
		create DAG edge from key2 to key1

功能：
	multi-thread 调度执行入度为0的leaf_key求值
	求值时如发现%%{} %%%{}引用依赖，则按需扩展DAG edge/node

基本流程：

可先MVP串行实现，后做并行化改造。

	evaluate_key(key):
		if key is already in progress
			wait config_space.$key:ready
		else
			load_configs(key)
			merge_values(key)
		return config_space.$key:value

	merge_values(key):
		collect_result = None
		for vhash in sort_values(config_space.$leaf_key:values)
			merge_one(key, vhash, collect_result)
		$leaf_key:value = collect_result

	sort_values(values_attr)
		refer to config_load.md ## merge 优先级

	merge_one(key, vhash, collect_result):
		when_cond = evaluate_when(vhash.when)
		return if !when_cond
		get key's merge policy func
		return merge_func(collect_result, evaluate_one(vhash.value))

	evaluate_when(when)
		like evaluate_one, with more var expand/search rules

	evaluate_one(key, val):
		expand_macro(val)
		if is python code
			return eval_python(val)
		else
			return val

	expand_macro(val):
		for each %%{} %%%{} referenced key in val:
			evaluate_key(ref_key) # XXX: turn into DAG scheduling
		replace %%{} %%%{} in val
		replace d.xxx, dd.xxx in python code
		return val

	eval_python(val):
		RPC call python interpreter

## python interpreter module

started by:
	main rust module
	can run multiple interpreter instances
on startup:
	import std libs (没有副作用)
	for all layers
		import lib/modulexxx.py
	listen for RPC request

members:
	imported modules/funcs

on RPC:
	eval(code)
	# code can directly call lib.xxx
	# code cannot do import

函数运行环境的纯净性和可重复性:
	import whitelist
	disable disk/network IO

函数purity测试:
	缓存每个函数的input/output，随机重复调用，检察是否完全不变

## pure function (run python in restricted mode)

防止副作用
可重现

有沙箱python方言，不过建议使用标准python。

starlark		https://github.com/google/starlark-go
RestrictedPython	https://restrictedpython.readthedocs.io/en/latest/idea.html

## dependency graph

需要建立各key之间、包文件之间、input file/option与output之间的依赖关系
用于
- caching
- on-demand file loading
- delayed evaluation

各function和delayed evaluation code之间的依赖关系和执行顺序，需要结合具体实现进一步梳理。
递归求值是一个选项。需要确定各function可能影响的field，登记为依赖项。
各field、function需记录evaluated, finalized属性作为递归结束条件。


parallel parse in package unit
tiny interpret for simple expressions
write python class/methods and call python interpreter for non-trivial logics
on error, save generated standalone python code for easy debug
define python read-only property
- d.version
- d['subpackage.devel.requires'] 
- dd['pkgs.bash.version'] 

## yaml + pure funcs model

all logic must be in
- impure standalone fetch/extract functions
- pure standalone functions
- pure yaml values

all refer to configuration space must be in
- yaml values

## architecture

module: the main RUST
- load/parse yaml files
- merge values
- find out depends
- create DAG execute plan
- run logics via RPC call to parallel python language servers

module: pure python language server
module: fetcher python language server (only need in future, at build time)

## build system

每个build system都设置自己的builder.sh/py，该脚本接受两种配置方式
1) YAML env.xxx, meta.env.xxx 字段，统一转换为环境变量env_xxx, meta_env_xxx
2) phase.sh/py 文件，由builder.sh/py source/import后，按需调用其中的钩子函数。

暴露给用户定制的use flags，通过transform函数或者宏引用，修改以上两者发生作用。

## main components

data
	config.yaml

	types/package.yaml

	use/<feature>.yaml

	pkgs/rpmbuild/<pkg>/<pkg>.yaml
	pkgs/rpmbuild/<pkg>/files.yaml
	pkgs/rpmbuild/<pkg>/phase.sh
	pkgs/rpmbuild/<pkg>/runtime-phase.sh
	pkgs/rpmbuild/<pkg>/changelog.md

	test/<scenario1>/<input files>
	test/<scenario1>/<output specs>
	test/<scenario1>/<config_space dump>

common infra
	ConfigSpace
	- hash CRUD ops

types/attrs
	CheckFuncs
	MergeFuncs
	TransformFuncs

DSL
	LibFuncs
	when condition
	macro evaluation
	python evaluation

register layer config files

	LayerLoader
	- find/load index.yaml

delayed evaluation

	YAMLLoader
	- include

Spec output

	SpecComposer

spec macro <> yaml customizable option
