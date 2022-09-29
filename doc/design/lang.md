# 语言选型

## 核心代码：优选rust

效率目标：对10万级软件仓，秒级响应，常见操作0.1秒级响应

只有静态编译语言，或者JIT javascript才能秒级加载1万个YAML，或者10万个JSON

因而YAML加载/合并的核心代码，建议用安全高效的rust

- rust: 开发效率低，安全，可处理动态yaml/json
- C++: 开发效率中，可处理动态yaml/json
- golang: 开发效率高，但无法处理动态yaml/json
- crystal: 开发效率最高，可处理动态yaml/json，但生态小众

实测数据：

1) Time to load 1000 yaml files (70倍差距):

	9.46s python
	0.13s crystal

2) Javascript JIT speed is close to crystal (can load 10000 yaml in 2s)

	node dump-yaml-10000.js  2.23s user 0.06s system 108% cpu 2.109 total

## 外围代码：优选python

外围代码可使用python，最流行的系统脚本语言。

## 配置代码：可选python/javascript

YAML配置文件中的代码，支持不同的项目按需选择python/javascript，但一个文件内只能选其中之一。
第一版只实现python。

因为
- 不同的项目/社区，对脚本语言的偏好有多样性
- OS牵涉广泛的用户和维护者，也会有各自的语言选择
- javascript+python will have very good user base coverage
- javascript相对来说，有很好的配置语言特性: sandbox, functional, expressive

维护问题：公共函数可优选写python function，借助工具自动转换为javascript function

样例：python dict不如javescript优雅

javescript:

定义：
	user = {
	  firstName: "Angela",
	  lastName: "Davis",
	  role: "Professor",
	}
引用：
	user.role

python dict: 必需明确使用字符串格式

定义：
	tinydict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
引用：
	print "tinydict['Name']: ", tinydict['Name']

## 配置文件格式：YAML及JSON/JSONNET/TOML/CUE等可转换格式

除了直接加载YAML，未来可以支持其它YAML兼容的格式，例如JSON/JSONNET的格式。

例子：webpack 接受以多种编程和数据语言编写的配置文件。
https://www.webpackjs.com/configuration/configuration-languages/

YAML主要用于基本包; JSON主要用于缓存; 其它格式主要用于用户自写自用配置文件。

End user should be able to choose his favority language (python, typescript,
jsonnet) to write user configuration. Then generate JSON and merge with YAML.

User can define their own config in yaml/toml/json/jsonnet/dhall etc.
  whatever can be converted to yaml
  botton layer (eg. bb, not bbappend) should be dumb formats
  jsonnet/dhall mainly useful for end-user or iso/repo level configuration

样例：

https://reflect.run/articles/typescript-the-perfect-file-format/

	Here’s that same “schema” in Typescript:

	interface MyAppConfig {
	  locale: string,
	  timezone: string,
	  logLevel: 'trace' | 'debug' | 'info' | 'warn' | 'error' | 'fatal',
	  environment: 'local' | 'dev' | 'staging' | 'production',
	}

## rust -- javascript interaction

https://www.secondstate.io/articles/embed-javascript-in-rust/
https://github.com/second-state/wasmedge-quickjs/

	fn js_hello(ctx: &mut Context) {
	    let code = r#"print('hello quickjs')"#;
	    let r = ctx.eval_global_str(code);
	    println!("return value:{:?}", r);
	}

## language native attributes 

ruby: method_missing

python: __getattr__
https://docs.python.org/3/reference/datamodel.html#object.__getattr__

js: proxy
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy#finding_an_array_item_object_by_its_property

