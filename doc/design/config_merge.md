# 配置分层与合并

## 有意义的合并

per-field定义type和merge属性，使得每个字段可以进行
- 自动类型转换
- 有意义的合并

例子1：

	baseos/package.yaml
		buildRequires: a

	overlay/package.yaml
		buildRequires: b
		(此处不必使用类似yocto的BuildRequires:append)

	=>
	output/package.yaml
		buildRequires: a, b

例子2：

	overlay1/package.yaml
		use.pgm: false
	overlay2/package.yaml
		use.pgm: true
	overlay3/package.yaml
		use.pgm: false

	=>
	output/package.yaml
		use.pgm: true

此处configure flags的默认merge策略可设为 “向需要该功能的看齐”。
各overlay只需表述其需求，
- 有的希望做裁减，设置false
- 有的依赖该功能，设置true
最终得到有意义的全局统筹结果，而不依赖谁先提需求，谁后提需求。
当系统长大，这一能力非常重要。使多方定制变得简单，有序，易协调，可预期。

## overlay定义option的能力

Base OS的软件包如果写成这样(RPM)：

	%configure \
	%if %{with pgm}
		    --with-pgm \
		    --with-libgssapi_krb5 \
	%endif
		    --with-libsodium \
		    --with-openssl \

或者这样(Nix)：

	buildInputs = [ pcre pcre.dev libxml2 zlib bzip2 which file openssl ]
		     ++ lib.optional enableDbi libdbi
		     ++ lib.optional enableMagnet lua5_1
		     ++ lib.optional enableMysql libmysqlclient
		     ++ lib.optional enableLdap openldap
		     ++ lib.optional enablePam linux-pam

那么如果后面一个overlay想增加一个定制use.ssl，怎么办？
把base os的大块代码复制过来，然后局部修改？这违反了DRY原则，将对理解和维护造成困难。

解决方案是让merge function根据use.ssl的true/false，
明确添加/删除buildInputs字段的openssl元素。
这样一来，原始的buildInputs写法可以简化，条件代码挪到各option处。

## data pipeline 层间引用

上层overlay里的字段code，应该可以通过"prev."前缀，引用下层overlay的字段值。
l1.key1
l2.key1
l3.key1 {prev => l2.key1}

## each layer has a name

So that one can replace item of an exact layer.
So that one can insert item after an exact layer.

## origin/update 包文件的自动识别

一个YAML文件，可以定义一个软件包，也可以对另一个软件包做局部修改。
我们用如下两个概念加以区分：
- origin package file是一个软件包的原始定义。
- update package file是对（第三方）原始定义的补充与修改。
它们可以类比yocto里的bb与bbappend文件。

这里我们不采用bb/bbappend这样，以文件后缀名来区分origin/update，而是认为可以自动判断：
如果一个YAML包文件里定义了meta.xxx (spec:Summary/License/URL)这些字段，那么就认为它是origin package。
因为这些字段一旦定义，一般第三方没必要去修改。

## 通常在baseos、origin package YAML内描述多版本、多架构处理逻辑

描述特定版本、架构的处理(如打patch)逻辑
这些是软件包本身属性，应该在origin package定义，方便各overlay/project共享。

各overlay/project主要聚焦定制option (expected customization)，
以及原package未考虑到情形的fixup  (unexpected customization)。

理想情况下，overlay应该只需修改version，而不必操心该version依赖哪些bug fix patch.
当然overlay如果想自己加feature patch，那完全可以。

长期目标，实现脚本化更新版本列表，可DB搜索与指定安装具体版本。

## delayed evaluation

YAML内嵌python code表述了各field之间的内在逻辑关系。
所以应该在merge结束之后进行求值，才有意义。

还有利于减负增效。

## inherit 字段

用法

	inherit: source.path

从指定的global config-space path继承所有k/v到当前path

功能对比:
- inherit 要求等待 source.path 所有相关文件load结束，非常适合带抽象的全局引用
- include 在当前YAML文件加载时立即执行，只适合引用当前目录下的强相关/附属文件

## merge 优先级

每一个配置文件需要包含一些属性，传递到所属各字段，以便确定它们在override层级中的位置。

第一优先级：origin package < update package
第二优先级：docType order
第三优先级：layerPrio 数字序
第四优先级：layerName 字典序

docType 按优先级顺序从高到低定义如下：

	env-user
	env-project
	env-system
	build
	distro
	hw-machine
	hw-board
	hw-chip
	hw-arch
	sw-package
	base

注意docType是对应到每个YAML的，不是绑定一个固定的docType到layerName。
一个git repo应当合理安排目录结构，不同docType的YAML文件分目录聚类存放，以便给各YAML批量加上合适的docType字段。

上述顺序的基本原则是：
- 从上到下，一般是N:1的关系
- 从上到下，可以鸟瞰下面各层的配置代码; 反之下面layer的开发者不一定知道上面开发者/用户的配置和用法。
- 因而从上到下override比较合适

上述排序原则，相对yocto，做了如下两点改进：

1) layers顺序必需由其内在属性决定，不受用户配置文件中先后顺序的影响。
避免让最终用户指定层级顺序，以避免随机性，简化用户配置，使能全局自动化测试。
这样社区的大量第三方layers，可以消减排序这个维度的不确定性和组合爆炸问题，减少未经测试的bug。

2) layerPrio number不好理解、把握、协调。因而我们在它之上新增一个docType维度的排序，将priority number置于次要地位。如果必要，进一步替代priority number的可能办法是，对well known layers，协调设置它们之间的依赖关系，作为merge排序依据。

references
这里我们把yocto 的 layer type 细分为了 doc type.

https://www.openembedded.org/wiki/Layers_FAQ
How do I choose the appropriate "layer type" for my layer?

    Base: this is really only for oe-core and meta-oe, i.e. the base metadata for the build system.
    Machine (BSP): if your layer primarily exists to add support for additional machine(s), use this type.
    Software: if your layer primarily provides recipes for building additional software, use this type.
    Distribution: if your layer primarily provides policy configuration for a distribution (conf/distro/*), which may include customised/additional recipes for the distribution, then choose this type.
    Miscellaneous: if your layer doesn't fall into any other category you can choose this type; however there shouldn't be too many miscellaneous layers and it may be an indication that the purpose isn't well defined or that you should consider splitting the layer.


## 取值空间极其删减

对一个包的一个字段的定制，涉及以下几个维度
1) default value(s): 取值范围是客观的，值的先后顺序可以是主观的
   - :type
   - :default
   - :defaults/:values/:ranges
2) 客观约束: 在baseos描述现实世界的各类约束，依赖以及非法组合
   - :excludes
3) 主观意愿: 在各layer表达定制需求
   - :append/:prepend
   - :remove/:replace

在(1)中，当一个字段的:type为bool时，以下两者等价

	:default: true
	:defaults: [true, false]

## excludes 字段

这是一种用户友好形式，以简单灵活的方式，定义一组非法组合。
实现中会通过transform函数，转换为对应字段的:excludes属性。

其取值为数组，其中每个item由1-3部分构成，基本形式如下

	excludes:
	- simple-condition  when multi-condition  // message

其中的
- simple-condition 是必选项，表达一个字段的取值条件
- when multi-condition 是可选项，表达一个when condition
- // message 是可选项，表示提示消息

样例

```
	conflicts("%clang@:7")
	conflicts("%gcc@:5.0", when="@8:")
	conflicts("%oneapi@:2022.1.0", when="+fortran")
	conflicts("+openmp", when="%clang", msg="OpenMP not available for the clang compiler")
	conflicts("+openmp", when="%pgi", msg="OpenMP not available for the pgi compiler")
	conflicts("+shared", when="platform=darwin %gcc")
	conflicts("cxxstd=14", when="@1.8:")
	conflicts("platform=darwin", msg="ALSA only works for Linux")
=>
	excludes:
	- %clang@:7
	- %gcc@:5.0             when @8:
	- %oneapi@:2022.1.0     when +fortran
	- +openmp               when %clang     // OpenMP not available for the clang compiler
	- +openmp               when %pgi       // OpenMP not available for the pgi compiler
	- +shared               when platform=darwin %gcc
	- cxxstd=14             when @1.8:
	- platform=darwin                       // ALSA only works for Linux
```

## merge overrides: append/prepend/remove/replace属性及参数

把value放入key的append/prepend属性中去

	key:append
	key:prepend

merge顺序:

	merge(prepend-values, normal-values, append-values)

移除整个key：
	key:remove:

移除key里的一项内容：
	key:remove: item

remove item动作会在files load后，merge前进行。
remove key动作可以视情况优化提前。

如果未来需要的话，append/prepend属性还可以带参数

	key:prepend=item_value: val1
	key:append=item_value: val2

merge顺序：

	merge(other-normal-values, val1, item_value, val2, other-normal-values)

此时会先找到item_value所在位置, 然后将val1/val2插入其前后。

有时粗粒度的layer顺序不一定适用于某些特殊情况。
可以通过如下属性，精确设定一个key的merge顺序：

	key:prepend@layerName
	key:append@layerName

有时一个底层layer的key/condition设置考虑不周全，需要fixup。
可以通过如下属性，删除/替换特定layer的值：

	key:remove@layerName
	key:replace@layerName

@layerName的用法偏hack，应当限制使用：
- 只有 docType=env-xxx 的 layers (用户侧) 可以使用
- 其它 layers，提示warning，促使layer开发者与对应的别的layer协调后，做通用化改进，避免hack

## prepend不常用

基本只对PATH有用。 PATH:append只出现了4次。

	wfg /c/yocto% gr -h -o '^[a-zA-Z]+:prepend'|sc
	=>  127 FILESEXTRAPATHS:prepend
	      9 PACKAGESPLITFUNCS:prepend
	=>    7 PATH:prepend
	      6 PACKAGES:prepend
	      6 DEPENDS:prepend
	      1 PROVIDES:prepend
	      1 PREMIRRORS:prepend
	      1 MACHINEOVERRIDES:prepend
	      1 LDFLAGS:prepend
	      1 GOBUILDFLAGS:prepend
	      1 CFLAGS:prepend

## 定制场景化思考

Human is very bad at handling/anticipating combination explosion of layer overrides.
Better at understanding "demand list", simple aggregation.
Express needs (declarative) instead of changing things then collide.
原子化表达需求，尽量做到可与其它layer任意搭配

1)
避免careless override，将其视为conflict，并给出错误消息。

从yocto的统计来看，极少需要多次设定。可通过良好的设计安排来避免。
(bbappend文件数量只有bb文件的1/10，内容更少)

2)
很多字段(patches, phase scripts)都是数组类型，各layer只需定义好

	key when condition: item

即可新增自己关注的元素。在merge function的帮助下，即可做到互不干扰。
用户碰到问题，一般是condition部分没考虑特定场景，短期解决靠override，长期方案改进上游layer的condition即可。

3)
单次设定(no conflict)
- version
default value与单次设定同时存在，不是conflict
如果conflict难以避免，则可用key:replace来明确替换旧值。

4)
提供方-消费方
- options
- versions

5)
define-refine
- define方是official的，然而不是全知全能，可能会有遗漏
- refine方发现在特定场景下需要refine official的某个字段或其条件，可在自己配置文件中进行，并指定被refine的git repo

6)
对特定元素 refine rule
- patch
- cflag

7)
各layer都做加法，且是condition限定下的加法。
只在最后用户侧做必要的减法。
这样可以有效避免中间layers 做+/-的conflicts
eg.
	layer A want +CONFIG_XXX
	layer B want -CONFIG_XXX

对数组类型，mergePolicy=append|prepend类型的字段，多处地方的条件配置，最后效果是做加法，等同于||
	repo-a
		cflags when cond1: -g
	repo-b
		cflags when cond2: -g
=>
		cflags when cond1 || cond2: -g

对于用户，若想修正，做减法即可：
	user-config
		cflags:remove: -g

然后考虑更好的长期方案，给repo-a/b提交补丁，完善其cond1/cond2。
长期推动各方认真思考和改进condition，避免无脑+/-，置社区于浑沌。
