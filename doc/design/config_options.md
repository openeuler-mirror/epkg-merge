# 软件包定制选项

原则上所有YAML包字段都可以被定制覆盖。
它们大体上可以分为以下几类
- 固定字段
- 构建脚本接受的phase.xxx
- 构建脚本接受的env.xxx
- use flags

其中，用户一般希望能够
- 查询列出versions，并定制固定字段 version
- 查询并定制use flags

## 自定义构建选项 use.*

每个包可以自定义构建参数。

在软件包YAML中，可以通过定义如下attributes来定义一个用户可定制的构建选项。
其中key的形式是: use.your-flag-name

	    key:type
	    key:default
	    key:example
	    key:doc
	    key:checkFunc
	    key:checkParams

use字段经由如下方式之一对影响构建行为：
- %%{use.xxx} 宏替换，一般用于phase.xxx
- 通过transform函数，修改env.xxx，进而影响引用这些env的builder script

可以直接修改CFLAGS等env变量实现的定制，就不要使用use。
还有一些不宜在包中引入use flags的场景，可以参照如下gentoo指南：
https://devmanual.gentoo.org/general-concepts/use-flags/#when-not-to-use-use-flags

## 快速自定义 use 开关量

spec样例
	定义参数
		%bcond_with bootstrap	# defaults value to 0
		%bcond_without ncurses	# defaults value to 1
	使用参数
		%if %{with ncurses}

我们希望yaml可以这样写
	定义参数
		useFlags:
			-bootstrap: do initial bootstrap build
			+ncurses: use ncurses library
	一般形式
		useFlags:
			[+-]<option>: <one-line doc>
	使用参数
		key when +ncurses: val

useFlags的底层实现，是通过transform函数添加如下字段

	    use.ncurses:type: bool
	    use.ncurses:default: true
	    use.ncurses:doc: use ncurses library
	    use.ncurses:mergeFunc: merge_policy_or

## 快速自定义 use 选项

定义参数

	use:
		cxxstd:doc: use the specified C++ standard when building
		cxxstd:type: int
		cxxstd:is_oneof: [11, 14, 17, 20]
		cxxstd:default: 20
使用参数

	key when cxxstd=20: val

## 定义 configure flags

对最常见的 configure flags, 可以特别定义 useConfigureFlags

参照yocto

	PACKAGECONFIG ??= "f1 f2 f3 ..."
	     PACKAGECONFIG[f1] = "\
				  --with-f1, \
				  --without-f1, \
				  build-deps-for-f1, \
				  runtime-deps-for-f1, \
				  runtime-recommends-for-f1, \
				  packageconfig-conflicts-for-f1 \
				  "
	     PACKAGECONFIG[f2] = "\
				 ... and so on and so on ...

我们引入如下字段来实现类似功能：

	useConfigureFlags:
		f1: description-f1, --with-f1,   --without-f1, build-deps-for-f1, runtime-deps-for-f1, runtime-recommends-for-f1, packageconfig-conflicts-for-f1
		f2: description-f2, --enable-f2, --disable-f2, build-deps-for-f2, runtime-deps-for-f2, runtime-recommends-for-f2, packageconfig-conflicts-for-f2

Can prefix the f1/f2 key with +/- to set default to true/false.

通常 configure with/without或enable/disable flags 是对称的，此时可省略第三项，让工具自动推导。
后面的几个字段也不常用。所以一般看起来像这样

	useConfigureFlags:
		f1: description-f1, --with-f1,, build-deps-for-f1 
		f2: description-f1, --with-f2,, build-deps-for-f2 
		f3: description-f1, --with-f3,, build-deps-for-f3 
		f4: description-f1, --with-f4,, build-deps-for-f4 
		f5: description-f1, --with-f5,, build-deps-for-f5 
		f6: description-f1, --with-f6,, build-deps-for-f6 
		f7: description-f1, --with-f7,, build-deps-for-f7 

另一种可选方案类似函数调用的named parameter:

	useConfigureFlags:
		f1:
			doc: 		description-f1
			enable: 	--enable-f1
			disable: 	--disable-f1
			buildRequires: 	build-deps-for-f1 
			requires: 	runtime-deps-for-f1 
			recommends: 	runtime-recommends-for-f1
			conflicts: 	packageconfig-conflicts-for-f1
		f2:

这一形式稍显罗嗦，但有利于推广，因为小白用户也能一看便知，便能上手使用。

Looks more configurable than Gentoo's DSL:

	DEPEND="
		alsa? (
			media-libs/alsa-lib
			media-libs/libsndfile[alsa]
		)
		ao? (
			media-libs/libao
			media-libs/libsndfile
		)
		bidi? ( dev-libs/fribidi )
		gdk-pixbuf? (
			x11-libs/gdk-pixbuf-xlib
			>=x11-libs/gdk-pixbuf-2.42.0:2
		)

## 预定义全局use flags

大量的configure flags在各个项目里是通用的。这些可以通过脚本自动生成一组配置文件

	configure_flags/<feature>.yaml
		cspath: use.<feature>
		useConfigureFlags:
			<feature>: ...

然后将它们作为base layer的一部份，由LayerLoader预加载到配置空间。

参考：Gentoo 定义了369个全局use flags，所有包加起来用了9600+ use flags。
这么多的use flags，用工具维护更scale，也更靠谱。

通常应避免指定 per-package defaults -- per-package feature should uniformly
default to global use default value.

## iuse 字段: 复用全局预定义use

一个软件包，可通过iuse字段声明要复用的全局use flags。

Gentoo样例：

	app-benchmarks/sysbench/sysbench-1.0.20-r100.ebuild
		IUSE="+aio attachsql drizzle +largefile mysql postgres test"

前缀+/-表示默认enable/disable该功能。

## uses 字段：批量设置use flags

未来如果有需要，可以引入如下字段及transform函数：

	pkgs.<pkg>.uses: +f1 -f2
=>
	pkgs.<pkg>.use.f1: true
	pkgs.<pkg>.use.f2: false

## 普适选项

每个包都可以有的定制项，不需要列到use下去。例如

	version
	buildRequires
	...

## 编译选项

这些编译器选项，由各底层构建脚本开放给上层定制:

          cflags, cxxflags, fflags, cppflags, ldflags, ldlibs

各build system可将其经由transform机制自动加入所辖各包的env字段，对第三方开放定制。

## 构建选项

参考nixpkgs的Flags列表，这些由各build system自动加入相应包的env字段。
普遍使用的，可以全局预定义，各包按需引用。

wfg /c/NixOS/nixpkgs/pkgs% git grep -ho '[a-zA-Z]\+Flags'|sc
   1889 configureFlags
   1626 makeFlags
   1192 cmakeFlags
    481 installFlags
    354 buildFlags
    300 mesonFlags
    228 pytestFlags
    100 qmakeFlags
     90 npmFlags
     86 checkFlags
     61 setOutputFlags
     57 patchFlags
     41 testFlags
     35 sconsFlags
     34 setupPyBuildFlags
     26 cargoBuildFlags
     23 wafConfigureFlags
     23 makeMakerFlags
     22 supportFlags
     22 nativeToolchainFlags

## env.configureFlags spec转YAML定制

原spec
	%conf
	%configure \
	%if %with_ssl
		--enable-ssl
	%end

YAML

	use.ssl: true
=> transform to
	env.configureFlags: --enable-ssl
=> used by build phase script
	phase.configure: %configure %%{env.configureFlags} 

新spec
	%conf
	%configure --enable-ssl

未来自研builder，可使用环境变量形式

	./configure ${env_configureFlags}

## YAML定制打通rpm spec宏定制

基本思路：rpm spec里的宏定制变量与判断，尽量迁移到YAML.
备选思路：难度大的情况，根据YAML field定义rpm macro，spec里继续按原样引用macro

条件判断
	%if
	%ifarch
	%ifnarch

开关定义
	%bcond_with
	%bcond_without

包内宏定义
	%global
	%define

样例
	%if %{with bootstrap}
	%global golang_bootstrap 0
	%else
	%global golang_bootstrap 1
	%endif

代价：所有%if后的rpm macro name都需要替换，且涉及全局宏变量，牵扯范围会很广！
统计：

	wfg@crystal ~% rpm --showrc|wc -l
	1781

	wfg /c/fedora% gr -h '^%if' */*.spec|sc|head -n50
	    288 %if 0%{?fedora}
	    175 %if %{with python3}
	    146 %if 0%{?suse_version}
	    140 %if 0%{?rhel}
	    132 %if %{with bootstrap}
	    123 %if !0%{?rhel}
	    110 %if %{with python2}
	     87 %ifarch x86_64
	     78 %if 0%{?fedora} || 0%{?rhel} > 7
	     75 %if 0%{?rel_build}
	     73 %if %{without bootstrap}
	     73 %if %{with doc}
	     67 %if %{revision} >= 50
	     64 %ifarch s390x
	     60 %if 0
	     59 %if 0%{?rhel} && 0%{?rhel} <= 7
	     57 %if %{with tests}
	     55 %ifarch %{ix86}
	     53 %ifarch %{ix86} x86_64
	     53 %if 0%{?fedora} || 0%{?rhel} >= 8
	     52 %if 0%{?rhel} == 7
	     51 %if %{with check}
	     51 %ifarch %{arm}
	     49 %ifarch aarch64
	     46 %ifarch s390 s390x
	     45 %ifnarch s390 s390x
	     43 %if 0%{?with_selinux}
	     41 %if 0%{?el7}
	     39 %if 0%{?with_python3}
	     39 %if 0%{?fedora} || 0%{?rhel}
	     38 %ifarch %{ocaml_native_compiler}
	     38 %if ! 0%{?rhel}
	     36 %if 0%{?tests}
	     36 %if 0%{?flatpak}
	     35 %ifarch ppc64le
	     35 %if 0%{?gitdate}
	     33 %if 0%{?wine_staging}
	     33 %if 0%{?use_gitbare}
	     33 %if 0%{?bootstrap}
	     31 %if %{__with_wxwidgets}
	     30 %if %{with_systemd}
	     29 %if !%{disable_python3}
	     28 %if %{with docs}
	     27 %ifarch armv7hl
	     27 %if ! 0%{?bootstrap}
	     26 %if 0%{?with_python2}
	     25 %if %{without compat_build}
	     25 %ifarch sparcv9 ppc
	     25 %ifarch %{arm} aarch64
	     24 %if 0%{?rhel} && 0%{?rhel} < 8
	     
	  wfg /c/fedora% grep -ho -E -e '%[_a-zA-Z][_a-zA-Z0-9]+' -e '%{[?_a-zA-Z][ :_a-zA-Z0-9]+}' */*.spec |sort | uniq -c | sort -nr
	  55340 %{tl_version}
	  20165 %{name}
	  15251 %description
	  15004 %files
	  14463 %{_libdir}
	  13699 %{version}
	  12510 %package
	  10984 %{_texdir}
	  10685 %endif
	  10646 %{_datadir}
	  10064 %{buildroot}
	   9635 %{release}
	   9272 %if
	   8903 %license
	   7783 %{_mandir}
	   7505 %{_bindir}
	   7017 %global
	   5953 %doc
	   4495 %{_sysconfdir}
	   4302 %dir
	   3906 %{?_isa}
	   3534 %{_includedir}
	   2832 %changelog
	   2803 %{?dist}
	   2795 %{epoch}
	   2701 %install
	   2682 %build
	   2663 %prep
	   2315 %else
	   2072 %{_sbindir}
	   2030 %{source_date}
	   2021 %{_prefix}
	   2009 %config
	   1973 %{?rhel}
	   1888 %attr
	   1747 %define
	   1503 %setup
	   1477 %{_libexecdir}
	   1368 %{?fedora}
	   1355 %configure
	   1319 %ldconfig_scriptlets
	   1229 %autosetup
	   1212 %{python3_sitearch}
	   1194 %make_build
	   1172 %check
	   1149 %ifarch
	   1071 %{_unitdir}
	   1034 %{winepedir}
	   1007 %post
	    965 %{winesodir}
	    909 %make_install
	    834 %exclude
	    754 %{_localstatedir}
	    739 %ghost
	    723 %postun
	    710 %{?_smp_mflags}
	    659 %{shortname}
	    637 %find_lang
	    624 %{summary}
	    615 %{majorminor}
	    610 %bcond_without

### case 1: %if for fields

	%if !%{golang_bootstrap}
	BuildRequires:  gcc-go >= 5
	%else
	BuildRequires:  golang > 1.4
	%endif

思路：替换golang_bootstrap为YAML field, 然后使用when condition

### case 2: %if in scriptlets

被转为YAML field的rpm macro，该变量在出现的地方，我们都需要能处理

	%build

	%if !%{golang_bootstrap}
	export GOROOT_BOOTSTRAP=/
	%else
	export GOROOT_BOOTSTRAP=%{goroot}
	%endif

思路：支持字符串中的%if条件语句

## reference: Gentoo

https://devmanual.gentoo.org/general-concepts/dependencies/index.html

https://www.gentoo.org/support/use-flags/
/c/gentoo/gentoo/profiles/use.desc

	X - Add support for X11
	Xaw3d - Add support for the 3d athena widget set
	a52 - Enable support for decoding ATSC A/52 streams used in DVD
	aac - Enable support for MPEG-4 AAC Audio

/c/gentoo/gentoo/app-shells/zsh/zsh-9999.ebuild

	src_configure() {
		local myconf=(
			--bindir="${EPREFIX}"/bin
			--libdir="${EPREFIX}"/usr/$(get_libdir)
			--enable-etcdir="${EPREFIX}"/etc/zsh
			--enable-runhelpdir="${EPREFIX}"/usr/share/zsh/${PV%_*}/help
			--enable-fndir="${EPREFIX}"/usr/share/zsh/${PV%_*}/functions
			--enable-site-fndir="${EPREFIX}"/usr/share/zsh/site-functions
			--enable-function-subdirs
			--with-tcsetpgrp
			--with-term-lib="$(usex unicode 'tinfow ncursesw' 'tinfo ncurses')"
			$(use_enable maildir maildir-support)
			$(use_enable pcre)
			$(use_enable caps cap)
			$(use_enable unicode multibyte)
			$(use_enable gdbm)
		)

		if use static ; then
			myconf+=( --disable-dynamic )
			append-ldflags -static
		fi             

## reference: nixos

https://ryantm.github.io/nixpkgs/stdenv/stdenv/

## reference: buildroot

/c/buildroot/package/zsh/Config.in

	config BR2_PACKAGE_ZSH
		bool "zsh"
		depends on BR2_USE_MMU # fork()
		select BR2_PACKAGE_NCURSES
		help
		  zsh is a shell designed for interactive use, although it is
		  also a powerful scripting language. Many of the useful
		  features of bash, ksh, and tcsh were incorporated into zsh;
		  many original features were added.

		  http://www.zsh.org/   


/c/buildroot/package/zsh/zsh.mk

	ifeq ($(BR2_PACKAGE_PCRE),y)
	ZSH_CONF_OPTS += --enable-pcre
	ZSH_CONF_ENV += ac_cv_prog_PCRECONF=$(STAGING_DIR)/usr/bin/pcre-config
	ZSH_DEPENDENCIES += pcre
	else
	ZSH_CONF_OPTS += --disable-pcre
	endif

/c/buildroot/package/zstd/zstd.mk

	ifeq ($(BR2_PACKAGE_LZ4),y)
	ZSTD_DEPENDENCIES += lz4
	ZSTD_OPTS += HAVE_LZ4=1
	else
	ZSTD_OPTS += HAVE_LZ4=0
	endif

## reference: yocto

/c/yocto/yocto-docs/documentation/ref-manual/variables.rst

mutiple packages:
/c/yocto/meta-virtualization/recipes-containers/lxc/lxc_git.bb

