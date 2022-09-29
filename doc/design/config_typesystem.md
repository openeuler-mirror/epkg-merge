# 类型系统 type system

## 基本数据类型属性: type/checkFunc/mergeFunc

与类型相关的几个属性及其取值如下：

	:type 属性
		bool
		str (default)
		int
		float
		strSet (字符串集合，保序，无重复)

	:checkFunc 属性
		str:
			is_oneof(list)
			is_someof(list, separator=',')
			is_pattern(regex)	# matches regex
			is_package		# package name
			is_path			# path name
			is_PATH			# shell PATH
			is_version		# version string
			is_release		# RPM release string
		int:
			is_between(min, max)

	:mergeFunc 属性
		# default behavior is
		# - replace for basic types
		# - append  for array types
		# 请勿设置以上缺省值，以利于未来演进
		str:
			replace
			concat(sep) 	# ensures unique parts
		strSet:
			append		# ensures unique items

其中引用的函数，一般直接在rust定义，以达到最高效率。

带参数的:checkFunc，适合直接作为字段属性，如

			key:is_oneof: [a, b, c]
			key:is_someof: [[f1, f2, f3], ',']

这样用起来更加方便，且可以多个check效果叠加。

## 高级数据类型

在config space预定义如下常见高级类型

	types.path:type: str
	types.path:checkFunc: is_path
	types.path:doc: filesystem path name
	types.path:example: pkgs/bash/bash.yaml

	types.PATH:type: str
	types.PATH:checkFunc: is_PATH

	types.package:validSubkeys: name version versions release meta source patchset requires buildRequires subpackage phase runtimePhase includePhase includeRuntimePhase includeLib files use env ...
	types.package.name:type: str
	types.package.version:type: str
	types.package.version:checkFunc: is_version
	types.package.release:type: str
	types.package.release:checkFunc: is_release
	types.package.meta:type: str
	types.package.phase:type: str
	types.package.phase:mergeFunc: concat
	types.package.phase:mergeParams: "\n"
	types.package.includePhase:type: str
	types.package.includePhase:checkFunc: is_path
	types.package.includePhase:transformFunc: transform_phase
	...

## 节点属性搜索路径

搜索规则
1) 直接查找key:<attr>
2) 查找key:referAttrs
3) 查找parentKey:referAttrs
4) 若(2,3)找到:referAttrs，则查找路径替换后的redirectedKey:<attr>
5) 找到第一个非空项即成功退出

	pkgs.bash.phase.build:type <not found>
	pkgs.bash.phase.build:referAttrs <not found>
	pkgs.bash.phase:referAttrs = types.package.phase <found, redirect>
	types.package.phase:type = str <found, finish>

	pkgs.bash.version:checkFunc <not found>
	pkgs.bash.version:referAttrs <not found>
	pkgs.bash:referAttrs = types.package <found, redirect>
	types.package.version:checkFunc = is_version <found, finish>


## reference: NixOS

	/c/NixOS/nixpkgs/lib/types.nix
	wfg /c/NixOS/nixpkgs/nixos% g -e '^##' -e '^`types\.' doc/manual/development/option-types.section.md
	## Basic Types {#sec-option-types-basic}
	`types.bool`
	`types.path`
	`types.package`
	`types.anything`
	`types.attrs`
	`types.int`
	`types.ints.{s8, s16, s32}`
	`types.ints.unsigned`
	`types.ints.{u8, u16, u32}`
	`types.ints.positive`
	`types.port`
	`types.str`
	`types.lines`
	`types.commas`
	`types.envVar`
	`types.strMatching`
	## Value Types {#sec-option-types-value}
	`types.enum` *`l`*
	`types.separatedString` *`sep`*
	`types.ints.between` *`lowest highest`*
	`types.submodule` *`o`*
	`types.submoduleWith` { *`modules`*, *`specialArgs`* ? {}, *`shorthandOnlyDefinesConfig`* ? false }
	## Composed Types {#sec-option-types-composed}
	`types.listOf` *`t`*
	`types.attrsOf` *`t`*
	`types.lazyAttrsOf` *`t`*
	`types.nullOr` *`t`*
	`types.uniq` *`t`*
	`types.unique` `{ message = m }` *`t`*
	`types.either` *`t1 t2`*
	`types.oneOf` \[ *`t1 t2`* \... \]
	`types.coercedTo` *`from f to`*

## reference: JSON schema

	https://json-schema.apifox.cn/

	{
	  "type": "object",
	  "properties": {
	    "builtin": { "type": "number" }
	  },
	  "patternProperties": {
	    "^S_": { "type": "string" },
	    "^I_": { "type": "integer" }
	  },
	  "additionalProperties": { "type": "string" }
	}

	{
	  "type": "object",
	  "properties": {
	    "name": { "type": "string" },
	    "email": { "type": "string" },
	    "address": { "type": "string" },
	    "telephone": { "type": "string" }
	  },
	  "required": ["name", "email"]
	}

	{
	  "type": "array",
	  "items": [
	    { "type": "number" },
	    { "type": "string" },
	    { "enum": ["Street", "Avenue", "Boulevard"] },
	    { "enum": ["NW", "NE", "SW", "SE"] }
	  ],
	  "additionalItems": false
	}

