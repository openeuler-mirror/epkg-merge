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
- ${{pkg.use.xxx}} 宏替换，一般用于phase.xxx
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
		defineFlags:
			-bootstrap: do initial bootstrap build
			+ncurses: use ncurses library
	一般形式
		defineFlags:
			[+-]<option>: <one-line doc>
	使用参数
		key when +ncurses: val

Examples:

	variant("apps", default=True, description="Install the HELICS apps executables")
	variant("apps_lib", default=True, description="Install the HELICS apps library")
	variant("benchmarks", default=False, description="Install the HELICS benchmarks")
	variant("c_shared", default=True, description="Install the C shared library")
	variant("cxx_shared", default=True, description="Install the CXX shared library")
	variant("zmq", default=True, description="Enable ZeroMQ core types")
	variant("tcp", default=True, description="Enable TCP core types")
	variant("udp", default=True, description="Enable UDP core type")
	variant("ipc", default=True, description="Enable IPC core type")
	variant(
	    "encryption",
	    default=True,
	    when="@3.2.0:",
	    description="Enable support for encrypted communication",
	)

=>

	defineFlags:
		+apps:       Install the HELICS apps executables
		+apps_lib:   Install the HELICS apps library
		-benchmarks: Install the HELICS benchmarks
		+c_shared:   Install the C shared library
		+cxx_shared: Install the CXX shared library
		+zmq: Enable ZeroMQ core types
		+tcp: Enable TCP core types
		+udp: Enable UDP core type
		+ipc: Enable IPC core type
	defineFlags when @3.2.0::
		+encryption: Enable support for encrypted communication

defineFlags的底层实现，是通过transform函数添加如下字段

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

对最常见的 configure flags, 可以扩展定义 defineFlags

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

	defineFlags:
		f1:
			doc: 		description-f1
			values:		# default to bool values: true false; otherwise is a list of words
			default:	true
			when:		f2=xxx	# f1 is only valid when f2 is xxx
		f1=true:
			configureFlags: --enable-f1
			buildRequires: 	build-deps-for-f1 
			requires: 	runtime-deps-for-f1 
			recommends: 	runtime-recommends-for-f1
			conflicts: 	packageconfig-conflicts-for-f1
		f2:
			configureFlags: --with-f2=${{pkg.use.f2}} # 当有若干values时，用该方式较方便

Can prefix the f1/f2 key with +/- to set default to true/false.
 
Trade-offs: on/off vs true/false

- on/off: may be more user friendly, as external user interface
- true/false: standard bool type, more consistent and transfer-able,
  internal implement friendly, making the below value passing possible:

	build.cmakeFlags:
		Hydrogen_ENABLE_MPC:     ${{pkg.use.mpfr}}
		Hydrogen_ENABLE_CUB:     ${{pkg.use.cuda or pkg.use.rocm}}
		Hydrogen_ENABLE_CUDA:    ${{pkg.use.cuda}}

这一形式相比yocto稍显罗嗦，类似函数调用的named parameter。
但灵活性和可演进性强，且有利于推广，因为小白用户也能一看便知大概含义，便能上手使用。

Also more configurable than Gentoo's DSL:

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

## 自动翻转 configure flags

完整的defineFlags定义样例：

	defineFlags:
		f1=true:
			configureFlags: --enable-f1
		f1=false:
			configureFlags: --disable-f1

可以发现，上述true/false两种情况下的configureFlags有一种对称性。
这是非常常见的情况，所以一般不必设置false时的configureFlags，让配置框架自动通过翻转f1=true.configureFlags的"enable"为"disable"得到。

翻转推导规则：

	f1=true.configureFlags	=> f1=false.configureFlags
	================================================
	--enable-xxx 		=> --disable-xxx
	--enable-xxx=val	=> --disable-xxx
	--with-xxx 		=> --without-xxx
	--with-xxx=val		=> --without-xxx
	--with-xxx=yes		=> --without-xxx
	...=yes 		=> ...=no
	...=true 		=> ...=false
	...=ON 			=> ...=OFF
	...=1 			=> ...=0

在上述规则下，可自动推导的情况(例子来自yocto)：

	PACKAGECONFIG[x11] = "--with-x=yes --enable-xlib,--with-x=no --disable-xlib,${X11DEPENDS}"
	PACKAGECONFIG[arc4] = "ac_cv_lib_bsd_arc4random_buf=yes,ac_cv_lib_bsd_arc4random_buf=no,libbsd"
	PACKAGECONFIG[hwdb] = "HWDB=yes,HWDB=no,udev"
	PACKAGECONFIG[egl] = "-Degl=yes, -Degl=no, virtual/egl"
	PACKAGECONFIG[test-nonsecure] = "-DTEST_NS=ON,-DTEST_NS=OFF"
	PACKAGECONFIG[gmp] = "--with-gmp=yes, --with-gmp=no, gmp"
	PACKAGECONFIG[lzo] = "LZO_SUPPORT=1,LZO_SUPPORT=0,lzo"
	PACKAGECONFIG[gnome] = "-Dgnome=true,-Dgnome=false"
	PACKAGECONFIG[x11] = "--with-x=yes --enable-xlib,--with-x=no --disable-xlib,${X11DEPENDS}"
	PACKAGECONFIG[png] = "--with-png=${STAGING_DIR_HOST}${prefix},--without-png,libpng"

不能自动推导的情况有：

	PACKAGECONFIG[userdb] = "--enable-db=db,--enable-db=no,db,"
	PACKAGECONFIG[x11] = "-Dglx=yes, -Dglx=no -Dx11=false, virtual/libx11 virtual/libgl"
	PACKAGECONFIG[speexdsp] = "--with-speex=lib,--with-speex=no,speexdsp"
	PACKAGECONFIG[ipv6] = "--enable-ipv6,--disable-ipv6 gl_cv_socket_ipv6=no,"
	PACKAGECONFIG[systemd] = "--with-systemdunitdir=${systemd_system_unitdir}/,--with-systemdunitdir="
	PACKAGECONFIG[msgcat-curses] = "--with-libncurses-prefix=${STAGING_LIBDIR}/..,--disable-curses,ncurses,"
	PACKAGECONFIG[libunistring] = "--with-libunistring-prefix=${STAGING_LIBDIR}/..,--with-included-libunistring,libunistring"

有的包采用了"--with-xxx=yes => --with-xxx=no" 的翻转形式，但也有个别包的翻转形式是--without-xxx。
对于autotools来说，两者正常情况下是等价形式。自动翻转统一翻转为--without-xxx，以方便学习使用。

## 预定义全局use flags

大量的configure flags在各个项目里是通用的。这些可以通过脚本自动生成一组配置文件

	configure_flags/<feature>.yaml
		cspath: use.<feature>
		doc: 		one-line summary string
		alt: 		feature-altname1, feature-altname2
		default:	true
		buildRequires: 	build-deps-for-feature
		requires: 	runtime-deps-for-feature

然后将它们作为base layer的一部份，由LayerLoader预加载到配置空间。
上述字段均来自defineFlags的子字段，仅新增了一个alt字段。

参考：Gentoo 定义了369个全局use flags，所有包加起来用了9600+ use flags。
这么多的use flags，用工具维护更scale，也更靠谱。

## 复用全局预定义use flags

一个软件包，可通过设置useGlobal字段，继承/复用一组全局use flags。

	defineFlags:
		# inherit 3 flags from pre-defined global use.xxx
		# setting f3's default to true btw.
		f1 f2 +f3:
			useGlobal: true

		f1=true: # can further customize the inherited flag
		   configureFlags: --enable-f1

可以在key部分写多个feature，从全局use.$feature路径同时继承多个全局feature。

可选前缀+/-表示在本包里默认enable/disable该功能。
通常应避免指定 per-package defaults -- per-package feature should uniformly
default to global use default value.

## 自动猜测 configure flags

先看一些gentoo的use统计：

	wfg /c/os/gentoo/gentoo% grep -h 'caps\?' */*/*.ebuild|sc
	     87         caps? ( sys-libs/libcap )
	     24         caps? ( sys-libs/libcap-ng )
	     13                 caps? ( sys-libs/libcap )
	      4         caps? ( >=sys-libs/libcap-2.1.0 )
	      3 RDEPEND="caps? ( >=sys-libs/libcap-2.24 )

	wfg /c/os/gentoo/gentoo% grep -h 'ncurses\?' */*/*.ebuild|sc
	     57         ncurses? ( sys-libs/ncurses:0= )
	     21         ncurses? ( sys-libs/ncurses:= )
	     16         ncurses? (
	     11         ncurses? ( >=sys-libs/ncurses-5.2:= )
	      6         ncurses? ( >=sys-libs/ncurses-5.9-r3:0=[${MULTILIB_USEDEP}] )
	      6         ncurses? ( sys-libs/ncurses:0 )
	      5         ncurses? ( sys-libs/ncurses:=[unicode(+)] )
	      5         ncurses? ( >=sys-libs/ncurses-5.9-r3:0= )

可见一个well known feature，在不同的软件包中，可能buildRequires多种三方库，或者一个库的不同版本。
这种情况下，可以这样配置
- 在global use中预定义最常见的buildRequires
- 一个软件包首先inherit该global flag，然后如有需要，可重定义其buildRequires子字段

再看另一类差异：

	# use_enable/use_with manual: https://devmanual.gentoo.org/function-reference/query-functions/
	wfg /c/os/gentoo/gentoo% grep -h 'use_.* caps' */*/*.ebuild|sc
	     14                 $(use_enable caps linux-caps)
	     11                 $(use_with caps cap) \
	      9                 $(use_with caps libcap) \
	      5                 $(use_enable caps cap) \
	      4                 $( use_with caps libcap ) \
	      4                 $(use_enable caps)
	      3                 $(use_with capstone)
	      3                 $(use_with caps libcap-ng)
	      3                 $(use_enable caps libcap) \
	      3                 $(use_enable caps capabilities) \
	      2                         $(use_enable caps setpriv)
	      2                 $(use_enable caps capabilities)
	      2                         $(use_enable caps capabilities)
	      2                 $(use_enable caps cap)

	wfg /c/os/gentoo/gentoo% grep -h 'use_.* ncurses' */*/*.ebuild|sc
	     10                 $(use_enable ncurses curses)
	      9                 $(use_enable ncurses) \
	      8                 $(use_with ncurses) \
	      7                 $(use_enable ncurses)
	      5                 $(use_enable ncurses curses) \
	      4                 $(use_with ncurses curses)
	      3                 $(use_with ncurses term) \
	      3                 $(use_enable ncurses consoleui)
	      2         local myconf=( $(use_enable ncurses ui) )
	      2         econf $(use_with ncurses curses)
	      2         econf $(use_with ncurses)
	      2                 $(use_with ncurses tinfo)
	      2                 $(use_enable ncurses term) \

可见同一个well known feature, 如caps，它在一个具体上游软件的configure选项，可以呈现多种形式

动词部分，以下均可能

	--enable/disable
	--with/without

名词部分，往往有几种常见名称

	--enable-linux-caps
	--enable-caps
	--enable-cap
	--enable-libcap
	--enable-libcap-ng
	--enable-capabilities

	--enable-ncurses
	--enable-curses
	--enable-term
	--enable-tinfo
	--enable-consoleui
	--enable-ui

以上动词、名词的不同形式，可以通过如下规则，较好的实现自动匹配，从而实现global use flag的较好复用
- 在global use flag预定义中，不预设configureFlags字段(因为形式太多样化了)，改为设置alt字段(如果有多个名词名字)
- 当configureFlags未定义，则在alt字段帮助下，在构建环境里通过解析`./configure --help`的输出，动态找到对应的configure option

举例说明。给定global use flag配置

	use.caps.alt: cap, capabilities, linux-caps, libcap, libcap-ng

则一个包继承该global use flag后，一般不需要设置configureFlags，
而是让构建系统在运行时自动在`./configure --help`输出里寻找如下正则表达式，找到一个即匹配成功：

	--(enable|disable|with|without)-(caps|cap|capabilities|linux-caps|libcap|libcap-ng)

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
	phase.configure: %configure ${{pkg.env.configureFlags}}

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

