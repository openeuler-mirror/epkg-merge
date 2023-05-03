# 定制友好的YAML+python

设计原则
- KISS
- understandable
- enough to meet 80% requirements

## YAML格式要求: 可脚本处理，包括read/write/update

常见的YAML template或者JSON DSL方案，容易写出update不友好的形式:

	% if condition
	key: 1
	% else
	key: 2
	% end

这样的YAML, 没办法经由

	load(); modify a field; save()

而仍然保留原YAML形式与逻辑，因而是update不友好的形式。需要加以避免。

样例：RPM不是YAML，但它的m4模板有类似形式：

	%if %{with pgm}
	BuildRequires:  openpgm-devel
	BuildRequires:  krb5-devel
	%endif

## YAML内置python code方式

事实上可以在提供update能力的同时，在YAML内(value部分)保有简单逻辑能力：

	key: {{1 if condition else 2}}
	key!: 1 if condition else 2

在此我们约定如下两种情况，解析为python表达式
- 包含{{ }}的字符串
- 以"!"结尾的key

{{ python-expression }} 会被替换为 repr(python-expression)
所以{{ }}中前后多余的空格不会被显示。

## 字段引用

按引用的场合方式，可分为两大类：
a) python code内无缝替换
b) 任意位置的宏替换

按引用的对象位置，可分为两大类：
1) 相对路径/局部访问：引用本文档内的key
2) 绝对路径/全局访问：引用全局config space的key

样例a1：
	k1: a string
	k2!: d.k1

样例a2：
	k1: 12
	k2!: dd.pkgs.bash.k1

此处
- "d" 对象 供python代码引用本YAML文档内任意字段
- "dd"对象 供python代码引用config space任意字段

在实现的时候，d/dd会被宏展开，但如果所引用的key是string类型，会自动加上""。

因而
- d.k1 会被展开为 "a string"
- dd.pkgs.bash.k1 会被展开为 12

样例b1：
	k1: xxx
	k2: %%k1

样例b2：
	k1: xxx
	k2: %%%dd.pkgs.bash.k1

此处
- %%fieldName （局部引用）会在任意位置被宏展开，替换为fieldName的值
- %%%pathName （全局引用）会在任意位置被宏展开，替换为 pathName的值

必要的时候，可以使用%%{}或者%%%{}。
%%/%%%与d/dd本质都是宏，区别是，展开时d/dd会判断值类型自动加""，而%%/%%%不会。

之所以不用%或者%{}，是因为它被RPM spec大量使用了，容易产生混淆。

我们的宏只出现在key/value部分，仍然是合法的YAML，是update友好的。

## 宏引用不存在的字段

当宏引用的key不存在时，系统将报错，以避免拼写错误等造成的静默bug。
通常空值(YAML null or python None)也意味着数据有问题，系统应当阻止其传播。
所以，系统提供如下设施，帮助处理可能不存在或者为空的字段。

- 对d/dd，提供get()/has()方法

	{{ d[key]	}} 	# raise error if key doesn't exist
	{{ d.get(key)	}} 	# return None if key doesn't exist, or was YAML null
	{{ d.has(key)	}}	# return True/False indicating whether key exists

- 对%%{}/%%%{}，增加filters机制 (prefer)

filters的优点是
- 一种通用机制，可对数据进行一系列操作
- 灵活、可扩展
- 不言自明，所有人可准确无误的理解

	%%{ key | default(0) }	# return 0 when key not exist/defined
	%%{ key | exists }	# whether key exists/defined

这里有一个可能的改进，就是会有很多判断型的filters，像ruby那样统一以问号做后缀，会比较清晰：

	%%{ key | exist? }	# whether key exists/defined

缺点是后台定义对应的python函数时，要做一个名字转换，因为python不支持带?的函数名。

Refer to
https://jinja.palletsprojects.com/en/3.0.x/templates/#jinja-filters.default

- 对%%{}/%%%{}，提供操作方法前缀(不推荐)

类似d.get(), d.has():

	%%{get:key}
	%%{has:key}

不如上面的数据流操作可扩展。

- 对%%{}/%%%{}，提供问号操作符(不推荐)

该可能性仅供参考。
该语法简洁，但不容易无歧义的被用户理解，不方便文档查询，也难以进一步扩展，
而后面几点远比语法表达少输几个字符重要。

%%{key?val1:val2}

	expand to val1, if key exists AND is not null
	expand to val2, if key does not exist or is null

容易发生理解歧义的地方：对exist/null/empty等情况下的确切行为，该返回val1还是val2还是报错? 不同的人可能有不同的想当然理解。

%%{key?}

	expand key, if key exists
	expand to nothing, if key's value is null/empty
	expand to nothing, if key does not exist

同样的功能，RPM macro用的是%{?key}形式，问号在前。
rust用的是问号在后的形式。
这种简单的加问号后缀形式，大概可以考虑支持。

%%{key}

	expand key, if key exists
	raise error, if key does not exist

Examples:

	"when %%{key?1:0}" detects whether key exists AND is not null
	"when %%{key?}"    detects whether key exists AND value != (null/empty, 0, false, off)
	"when %%{key}"     asserts key exists AND detects value != (null/empty, 0, false, off)

Reference: Conditionally Expanded Macros
https://rpm-software-management.github.io/rpm/manual/macros.html#expression-expansion

	Sometimes it is useful to test whether a macro is defined or not. Syntax

	%{?macro_name:value}
	%{!?macro_name:value}

	can be used for this purpose. %{?macro_name:value} is expanded to “value” if “macro_name” is defined, otherwise it is expanded to the empty string. %{!?macro_name:value} negates the test. It is expanded to “value” if macro_name is not defined. Otherwise it is expanded to the empty string.

	Frequently used conditionally expanded macros are e.g. Define a macro if it is not defined:

	%{!?with_python3: %global with_python3 1}

	A macro that is expanded to 1 if “with_python3” is defined and 0 otherwise:

	%{?with_python3:1}%{!?with_python3:0}

	or shortly

	0%{!?with_python3:1}

	%{?macro_name} is a shortcut for %{?macro_name:%macro_name}.

## 函数引用

YAML内置python code可以引用如下两类函数
	- rust内置函数，定义在lib/xxx.rs
	- python纯函数，定义在lib/xxx.py

引用方式为加lib.前缀：

	{{ lib.module1.func1(param) + "other python code" }}

实现方式为
- rust内置函数：宏替换
- python纯函数：python语言服务沙箱内解释执行

带副作用的函数，比如各种source fetcher，应该集中在核心代码仓定义。
各layer只能定义python纯函数，这样方便控制项目纯净度。

## 最大化可定制项，逻辑运算中间变量作为YAML字段可被overlay覆盖

如下形式的复杂数据变换逻辑链

	var1 = func1()
	var2 = func2(var1)
	var3 = func3(var2)

可用YAML表达为

	var1!: func1()
	var2!: func2(d.var1)
	var3!: func3(d.var2)

这样任何一个环节的数据，都可以被overlay定制。

最好进一步把中间变量放在特定名字空间下，以便设置规则，防止非预期的修改和环境变量污染。
并带上类型信息：

	var.str.var1!: func1()
	var.int.var2!: func2(d.var.str.var1)
	var.bool.var3!: func3(d.var.int.var2)

## 条件取值 (when condition in key)

有一种情况非常常见，对应yocto普遍使用的条件append:

	XEN_DEVICETREE_DOM0_BOOTARGS:append:juno = " root=/dev/sda1 rootwait"

值得在YAML中提供一种条件语法，具体是在key中加when条件

	key when condition: value

当条件表达式condition值为True时，等同于

	key: value

当条件表达式condition值为False时，等同于该行不存在。

例子：

	XEN_DEVICETREE_DOM0_BOOTARGS when board=juno: root=/dev/sda1 rootwait

condition语法：
1) k=v, 其中k是%%或者%%%宏
2) option=value，其中option是常见的global/package构建参数
	  global build parameters: target, board, platform, arch, os, 在build字段下搜索
	  package build option: eg. buildType, cxxstd, ..., 在pkgs.<pkg>.use字段下搜索
	  package builder ENV: compiler, configureFlags, ..., 在pkgs.<pkg>.env字段下搜索
3) +flag or -flag，其中flag是bool型的package build option，例如+debug -qt
4) @version-specs，例如
	@1.2:1.4 表示 version >= 1.2 and version <= 1.4
	@1.2:    表示 version >= 1.2
	@1.2     表示 version == 1.2
5) ^dependency-specs，例如 ^python@:3.3，表达依赖包的情况

Q: is the inclusive range enough?
A: Mostly. '>=' is dominant one, about 2 orders more than < and > and <=

	wfg /c/fedora% g 'Requires.* >= ' */*.spec|wc -l
	4241
	wfg /c/fedora% g 'Requires.* <= ' */*.spec|wc -l
	2
	wfg /c/fedora% g 'Requires.* < ' */*.spec|wc -l
	42
	wfg /c/fedora% g 'Requires.* > ' */*.spec|wc -l
	32

例子
	BuildRequires when +X: libx11
	BuildRequires when ^python@:3.3: py-enum34
	Patches when @0.2.5b8: gcc-5-compat.patch

yocto OVERRIDES example (used a lot)
bitbake/doc/bitbake-user-manual/bitbake-user-manual-metadata.rst
section Conditional Syntax (Overrides)

	# This yocto way can be confusing since it omits the key name.
	EXTRA_OECONF:append:linux-gnux32 = " --disable-asm"
=>
	EXTRA_OECONF when target=linux-gnux32: --disable-asm

## when expression

when支持and/or/not/()组合起来的复合表达式。优先级规则与python相同，从高到低为：

	()
	in, not in, <, <=, >, >=, !=, ==, =
	! x, not x
	&&, and
	||, or

这这里，我们选择同时支持and or not与 && || !，因为使用不同主力开发语言的开发者，可能有不同的习惯用法。
	ruby: 都支持
	python/jinja: 只支持 and or not
	js/github actions: 只支持 && || ! https://docs.github.com/en/actions/learn-github-actions/expressions

Rule1: =与==含义相同，因为不会在when里做赋值操作。

Rule2: 对
	word1 OP word2
word1/workd2均可以是如下明确形式
	- d/dd变量
	- %%/%%%变量
	- +flag/-flag
	- @version
	- ''/""字符串
	- 数字
如果出现非明确的形式，则约定word1是变量，word2是字符串。
这样方便书写如下形式的条件

	when target = linux-gnux32:
	when arch in aarch64 riscv:

Rule3: 真值、假值判断原则同python，但"off"作为假值处理
假值：null, None, False, false, 0, "", "off", [], {}

## when block

当同一个when条件影响多个字段时，用when block比较方便：

	OVERRIDES:append = "${ARM_AUTONOMY_HOST_OVERRIDES}"
	DEPENDS:append:autonomy-host = " dos2unix-native"
	SRC_URI:append:autonomy-host = " file://add-xen-support.patch;patchdir=../"
=>
	when %%ARM_AUTONOMY_HOST_OVERRIDES=autonomy-host:
		DEPENDS: dos2unix-native
		SRC_URI: file://add-xen-support.patch;patchdir=../

注意：这一能力先不实现，如果确实用的多，再考虑引入。

## python import modules/functions 列表

YAML python code应当是无副作用的纯函数，禁止访问本地存储、网络、时钟、随机数等外在数据源。
YAML python code里禁止自行import libs。只能使用python语言服务沙箱预加载的，无副作用的功能模块。

以下列表可按需补充：

	import string
	import re
	import math
	import collection
	import itertools
	import typing

## source fetcher 列表

常用source形式
	url
	git

不常用
	bzr
	cvs
	darcs
	github
	gitlab
	hg
	ipfs
	mavenartifact
	s3
	svn
	特定语言仓

## checkFunc 列表

输入：value + 额外参数
返回：True/False

	is_oneof(str, seq)
	is_pattern(str, regex)		# matches regex
	is_package(str)			# package name
	is_path(str)			# path name
	is_PATH(str)			# shell PATH
	is_version(str)			# version string
	is_release(str)			# RPM release string
	is_between(num, min, max)

## mergeFunc 列表

以下merge策略函数只应用于一次merge操作。

	merge_policy_concat(collect_str, new_val)
	merge_policy_append(collect_set, new_item)
	merge_policy_and(collect_bool, new_val)
	merge_policy_or(collect_bool, new_val)

完整的merge过程，需要初始化collect_str/collect_set，然后按顺序循环调用以上函数。

## transformFunc 列表

以下transform函数输入为字段值，输出为一个hash object。
调用方会把hash object转为key/val，供YAMLLoader插入当前YAML文档。

	# val example: "phase.sh"
	transform_include_phase(val)
		read shell script file
		yaml = {}
		for each shell function:
			yaml[func_name] = func_code
		return yaml

	transform_include_runtime_phase
	transform_include_lib
		它们可与 transform_include_phase 共享底层实现代码，只是加载的目标字段不同。

	# val example: "f1: this is some xxx feature, --with-f1,   --without-f1, build-deps-for-f1, runtime-deps-for-f1, runtime-recommends-for-f1, conflicts-for-f1"
	transform_use_configure_flags(val)
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

	# val example: "+X +ssl test"
	transform_iuse_flags(val)
		for each feature, output key/vals:
			inherit: use.feature
			use.feature:default: true/false if feature starts_with +/-

example:

	config space:

		use.ssl: { xxxx }

	pkg yaml:

		iuse: ssl
	=> (add key)
		inherit: use.ssl

## 字段属性列表

	:type
	:default
	:example
	:doc
	:checkFunc
	:checkParams
	:mergeFunc
	:mergeParams

	:transformFunc

	:fetcher

	:referAttrs

	:values

	:validSubkeys
	:loadedKeys
	:loadedAttrs
