# 配置空间

## config_space 数据结构

`config_space` 是一个全局Hash类型变量，承载本工具的核心概念。

`config_space` keys

	files."/a/b/c.yaml".cspath

	pkgs:type
	pkgs.bash:files
	pkgs.bash:type
	pkgs.bash:value
	pkgs.bash:layers
	pkgs.bash:referAttrs: types.package

	pkgs.bash.name: bash
	pkgs.bash.name:type: str

	types.package

	build.platform
	build.target

## a.b.c 形式路径引用

在加载各yaml文件时，记录各字段的完整a.b.c形式路径到一个Hash结构。
方便按路径直接引用。

同时记录a.b.c形式keys在一个搜索树，方便快速检索a.b下的所有keys。

There are 3 options to support this
- language native attributes
  - can only call all the way down the dependency chain and wait
  - non-keyword keys have to be accessed with d[key] or d.get(key)
- macro
  can create DAG then schedule expression evaluation in parallel
- DSL, a small python parser for yaml-value logics

Macro can take any form, like below. However best use the same form with
"language native attributes".

## key reference macros (obsolete)

在一个key的value部分和when condition部分，可以以如下形式引用其它key:

局部引用：
	anywhere:	%%{key}
	in python:	d.key; d['key']

全局引用：
	anywhere:	%%%{key.path}
	in python:	dd.key.path; dd['key.path']

局部引用样例：

	bash.yaml
		patchset.0 when %%version=1.1: some-file.patch

	其中%%version是本软件包名字空间的局部引用，会先加上包路径前缀pkgs.bash，扩展为全局路径pkgs.bash.version，在config space里求值

## key search path

key按需加载，遵循如下搜索流程

	pkgs.bash.version <not found>
	pkgs.bash.fspath <found, load bash.yaml under pkgs.bash config space path>
	pkgs.bash.version <found>
