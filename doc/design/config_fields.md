# YAML配置字段

## 命名规范

配置文件的字段名

1) 新增字段名，遵循一般配置文件命名习惯(比如k8s)，使用

	workingDir

而非

	WorkingDir
	working_dir
	WORKING_DIR

2) RPM spec原有字段名，可原封不动继承，亦可只继承名字，但统一使用新的camelCase命名风格。
建议统一，方便未来逐步脱离RPM体系。不至于新的体系从第一天开始就处于混乱(mixed)状态，徒增用户心智负担。

另外RPM spec里的字段定义和使用，本来就有诸多不一致。切换到YAML后，可借此机会尽量统一。

	Summary		CamelCase
	%description	lowercase

	Version		CamelCase
	%{version}	lowercase

	Source0		CamelCase
	%{SOURCE0}	UPPERCASE

## RPM spec fields mapping

	Name            =>  name
	Version         =>  version
	Release         =>  release
	Epoch		=>  epoch

	Summary         =>  meta.summary
	Group		=>  meta.group
	License         =>  meta.license 
	URL             =>  meta.homepage 
	%description    =>  meta.description  

	Source0         =>  source.0[:fetcher]
	Patch0          =>  patchset.0

	Provides        =>  provides
	Requires        =>  requires
	BuildRequires   =>  buildRequires
	(new) 		=>  testRequires
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

	%prep		=>  phase.unpack + phase.patch
	%conf		=>  phase.configure
	%build		=>  phase.build
	%install	=>  phase.install
	%check		=>  phase.check

	%files		=>  files
	%changelog	=>  放入独立changelog.md文件

	%pre		=>  runtimePhase.pre		
	%post		=>  runtimePhase.post		
	%preun		=>  runtimePhase.preun		
	%postun		=>  runtimePhase.postun		
	%pretrans	=>  runtimePhase.pretrans	
	%posttrans	=>  runtimePhase.posttrans	
	%verify		=>  runtimePhase.verify		

以下字段也置于runtimePhase字段下：

	%triggerprein
	%triggerin
	%triggerun
	%triggerpostun

	%filetriggerin
	%filetriggerun
	%filetriggerpostun
	%transfiletriggerin
	%transfiletriggerun
	%transfiletriggerpostun

Rare used ones:

	OrderWithRequires
	Prereq (obsolete)
	BuildPrereq (obsolete)
	BuildArchitectures
	Icon (obsolete)
	SourceLicense
	BugURL
	ModularityLabel
	DistTag
	VCS
	Distribution
	Vendor
	Packager
	NoSource
	NoPatch
	DocDir
	RemovePathPostfixes
	AutoReqProv
	AutoReq
	AutoProv
	ExcludeOS
	ExclusiveOS
	Prefixes/Prefix
	%generate_buildrequires

## 依赖类型标注?

	provides: lib() # 包含.so
	provides: cmd()
	provides: file() # 以/开始
	provides: api() resource() cap()

	requires: lib()
	requires: cmd()
	requires: file()
	requires: api() resource() cap()

## meta 字段

meta.xxx 适用于给人看的一般信息
- won't impact build process
- don't need change by 3rd party, so can be used for detecting whether a YAML file is origin/update package
- meta.env.xxx 可用于设置不影响最终制品包的环境变量 (ENV variables that won't impact build output)，如某些路径名.

## Requires() 字段

这些()条件

	cups/cups.spec
		Requires(pre): systemd
		Requires(post): systemd
		Requires(post): grep, sed
		Requires(preun): systemd
		Requires(postun): systemd

YAML里可体现为

		Requires: (pre):systemd
		Requires: (post):systemd
		Requires: (post):grep, (post):sed
		Requires: (preun):systemd
		Requires: (postun):systemd

## buildSystem 字段 (not now)

buildSystem可以大致分为如下类型

Make-based
- makefile

Make-incompatible
- ant
- maven
- scons
- waf

Build-script generation
- autotools
- cmake
- meson
- qmake
- sip

Language-specific
- clojure
- go
- guile
- haskell
- julia
- lua
- node
- ocaml
- octave
- perl
- python
- r
- racket
- ruby
- rust

Other
- bundle
- cuda
- emacs
- font
- gtk
- intel
- qt
- rocm
- texlive

不同 buildSystem 可以使用自己的公版build script，提供自己的构建参数，预定义自己的 build phases。
通过per-buildSystem模板与参数，有效简化per-package的配置。


## phase 字段

phase字段下，未来可以支持如下build phase/function name列表：

	unpack
	    preUnpack
	    postUnpack
	patch
	    prePatch
	    postPatch
	configure
	    preConfigure
	    postConfigure
	build
	    preBuild
	    postBuild
	check
	    preCheck
	    postCheck
	install
	    preInstall
	    postInstall
	fixup
	    preFixup
	    postFixup
	installCheck
	    preInstallCheck
	    postInstallCheck
	dist
	    preDist
	    postDist

reference：nixpkgs的build phases相当丰富，且一致性较好，值得借鉴。

	wfg /c/NixOS/nixpkgs/pkgs/stdenv/generic% g -e '^    runHook' -e '^.*Phase\()' setup.sh | tr -d '(){'

它允许各package以如下方式定制全部phases，或者局部(如preBuildPhases):

    if [ -z "${phases:-}" ]; then
        phases="${prePhases:-} unpackPhase patchPhase ${preConfigurePhases:-} \
            configurePhase ${preBuildPhases:-} buildPhase checkPhase \
            ${preInstallPhases:-} installPhase ${preFixupPhases:-} fixupPhase installCheckPhase \
            ${preDistPhases:-} distPhase ${postPhases:-}";
    fi

它也允许通过定义dontBuild等参数，选择性跳过一些phases:

        if [[ "$curPhase" = unpackPhase && -n "${dontUnpack:-}" ]]; then continue; fi
        if [[ "$curPhase" = patchPhase && -n "${dontPatch:-}" ]]; then continue; fi
        if [[ "$curPhase" = configurePhase && -n "${dontConfigure:-}" ]]; then continue; fi
        if [[ "$curPhase" = buildPhase && -n "${dontBuild:-}" ]]; then continue; fi
        if [[ "$curPhase" = checkPhase && -z "${doCheck:-}" ]]; then continue; fi
        if [[ "$curPhase" = installPhase && -n "${dontInstall:-}" ]]; then continue; fi
        if [[ "$curPhase" = fixupPhase && -n "${dontFixup:-}" ]]; then continue; fi
        if [[ "$curPhase" = installCheckPhase && -z "${doInstallCheck:-}" ]]; then continue; fi
        if [[ "$curPhase" = distPhase && -z "${doDist:-}" ]]; then continue; fi

## 映射 RPM spec 到 build systems and phases

1) 创建 buildSystem: rpmbuild
2) 映射 build phases

当buildSystem=rpmbuild时，有两种方案
1) 新增phase.prep，取代phase.unpack + phase.patch。
2) 自动识别%prep中的命令，把%setup放入phase.unpack，%patch放入phase.patch，其它语句酌情放入以上两个phase，或放入相应的pre/post phases。

如果自动化识别准确率高，优选方案(2)，为将来的分层定制预留空间。

	%prep		=>  (1) phase.prep or better (2) phase.unpack + phase.patch
	%conf		=>  phase.configure
	%build		=>  phase.build
	%install	=>  phase.install
	%check		=>  phase.check

## source 字段

有多个source时，提供机制给每个source命名。
对RPM spec，缺省进行Source0 => source.0的映射，也就是使用数字命名。

这样使其它layer容易使用名字来override。
在phase脚本内也方便引用${{pkg.source.0}}，相对而言，原spec引用方式是: %{SOURCE0}

	source.name1: url
	source.name1:md5sum:

	source.name2: url
	source.name2:dest:
	source.name2:md5sum:

## git 字段

一个上游软件，可以同时指定tarball URL和git URL。
前者使用source字段，一般内嵌version。
后者使用git字段，与commit一起使用。

	git.0:

对应

	source.0:

代表同一个上游软件。

git字段支持属性:
- commit
- branch
- tag
- submodules

commit/branch/tag只能设置其中一个。
其中commit可重复; branch不可重复; tag通常可重复，但没有保证。

## versions 字段：multi version 脚本化维护

多版本的常见需求是
1) 包维护者希望能自动收到上游版本更新通知
2) 用户希望能列出一个包的所有可用版本列表，并允许构建时从中选择一个版本
3) 选择版本时，别让用户操心要不要改增删一下补丁：这些内在逻辑依赖应该已经用条件表达式写在包YAML里

为解决诉求(1,2)，需要
- 引入versions.yaml，由工具自动化更新
- versions.yaml 内含 versions 字段定义

样例1: 传统tar包

	versions.'0.1.0'.sha256: b68239d67b2359ecc067cc354f86ccfbc8f02071e60d28ae0a2449f2e7f88001
	versions.'0.0.3'.sha256: d32052fbecd44299e13e69bf2dd7e5737c346404ccd784b8c2100ceed99d8cd3
	versions.'0.0.2'.sha256: b88357bf88cdda9565472543225d6b0fa50f0726f6e2d464c92d31a98b493abb

样例2: git branch/commit 以下建立了version值与git属性+值的关联

	versions.main.branch: main
	versions.'1.86.0'.commit: 9419cfa18c18dfbd1e1194127fd120ab456c3657
	versions.'1.82.0'.commit: d500b3363308f1f8ca70625c5cd10cce59b27641

btw, the '.' escape rule:
- treat . inside ''/"" as normal character

当用户指定了一个version, 对应的会创建如下属性之一，以确定下载方式。

	source.0:sha256: ${{pkg.versions.${{pkg.version}}.sha256}}
	source.0:sha256: ${{pkg['versions.' + pkg.version + '.sha256']}}  # another form, but not supported for now

	git.0:commit: ${{pkg.versions.${{pkg.version}}.commit}}
	git.0:branch: ${{pkg.versions.${{pkg.version}}.branch}}
	git.0:tag: ${{pkg.versions.${{pkg.version}}.tab}}

其中branch/tag不稳定，如需可重复，建议访问git服务，获取和设置当时对应的commit属性。

用户可以直接在version中指定git属性，方法如下

	version: commit:$commit # 如果是40字符完整commit，可支持省略前缀commit:
	version: branch:$branch
	version: tag:$tag

## source url中的version

根据源的不同，可以有多种形式指定上游项目下载地址

multi version中，某个具体version的url可以通过
- replace version in url
- compose git commit url
- compose github tarball url
等多种方式自动生成

特殊情况source url scheme发生变化：

	source.0: https://github.com/harfbuzz/harfbuzz/releases/download/${{pkg.version}}/harfbuzz-${{pkg.version}}.tar.xz
	source.0 when @:2.3.1: http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-${{pkg.version}}.tar.bz2

## patchset 字段

改patch粒度为patchset粒度，具体形式如下

	patchset.<patchset-name>: patches

patches经常是有一个版本适用范围的，可以用when condition来限定：

	patchset.<patchset-name> when @v1:v2: patches

## languages 字段

该字段可通过工具扫描source code tree，自动生成/校验/更新。
样例：

	languages: Ruby C Go Shell Makefile

本字段应当支持常用编程语言常见写法的归一化，比如Go写成go/golang应该都可以，加载后都归一化为Go
广义上，构建系统、单元测试框架的DSL也是语言，所以也一起列在这里。

这些语言和构建测试DSL，是一个软件的基本属性，可以自动检测，且衍生出对很多其他字段的默认定义。

## files 字段

spec:

	%files -f .mfiles
	%license LICENSE.txt NOTICE.txt
	%doc KEYS readme.html

	%files xsltc -f .mfiles-xsltc
	%license LICENSE.txt NOTICE.txt

	%files manual
	%license LICENSE.txt NOTICE.txt
	%doc build/docs/*

=>

in main yaml:

	include: files.yaml

files.yaml:

	files:rpm_macro_param: -f .mfiles
	files:
		%license LICENSE.txt NOTICE.txt
		%doc KEYS readme.html

	subpackage.xsltc.files:rpm_macro_param: -f .mfiles-xsltc
	subpackage.xsltc.files:
		%license LICENSE.txt NOTICE.txt

	subpackage.manual.files:
		%license LICENSE.txt NOTICE.txt
		%doc build/docs/*

参数暂存规则：如果%files带-f/-n等参数，则记录在`:rpm_macro_param`属性中，以方便转为spec的时候还原

## changelog.md 文件

changelog内容分开存放到changelog.md文件中去。它的内容适合存为 markdown 格式。

changelog.md不必加载到YAML，减少解析负担。

## subpackage 字段

spec:%package 转换为 YAML:subpackage
subpackage更贴合我们日常所说的"子包"，中英文一致，减少混淆。

## subpackages 字段

未来可参照nixpkgs的outputs字段:

	outputs = [ "bin" "dev" "out" "man" "doc" ];

按公共规则，自动构建对应的子包
