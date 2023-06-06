## rpmGlobal 字段：映射/传递 build options 到 spec

在包YAML中增加rpmGlobal小节，其中的key/val会被视为rpm macro，进而合入生成的spec文件。
其作用类似env环境变量，用于定制RPM spec。

	rpmGlobal:
		macroName: macro value

在各个包名字空间下的rpmGlobal，加到所生成spec的头部。
rpmGlobal尽量不暴露给用户或者第三方定制。避免在YAML字段中引用rpmGlobal字段下的值。相反，rpmGlobal可以引用其它字段。

数据流方向如下：

	customizable YAML fields
	=> pkgs.<pkg>.rpmGlobal 	=> spec header macro definitions

reference: define vs. global

	两者都可以用来进行变量定义，不过在细节上有些许差别，简单列举如下：

	    - define 用来定义宏，global 用来定义变量；
	    - 如果定义带参数的宏 (类似于函数)，必须要使用 define；
	    - 在 %{} 内部，必须要使用 global 而非 define；
	    - define 在使用时计算其值，而 global 则在定义时就计算其值；

	https://www.cnblogs.com/michael-xiang/p/10480809.html

## compiler cflags 定制

	rpmGlobal:
		__cc: ${{pkg.build.cc}}
		build_cflags: ${{pkg.build.cflags}}
		build_cxxflags: ${{pkg.build.cxxflags}}

## reference: 定制相关 rpm macros

https://src.fedoraproject.org/rpms/redhat-rpm-config/blob/rawhide/f/buildflags.md

Observation:
CFLAGS
- spec CFLAGS normally inherits one of %optflags/%build_ldflags/RPM_OPT_FLAGS/CFLAGS
- %build_ldflags inherits %optflags in global macros
- RPM_OPT_FLAGS inherits %optflags in %___build_pre
- CFLAGS inherits CFLAGS/%optflags in %cmake
- CFLAGS inherits CFLAGS/%build_cflags in %configure
- raw make without %configure will not inherit any contents in %optflags/%build_cflags
LDFLAGS
- spec LDFLAGS normally inherits %build_ldflags/RPM_LD_FLAGS
- RPM_LD_FLAGS inherits %build_ldflags in %___build_pre
CC
- no global macros for CC
- if spec need set CC, it just do it, so is not customizable

### CFLAGS in spec
	wfg /c/fedora% grep -w CFLAGS= c*/*.spec
	cachefilesd/cachefilesd.spec:   CFLAGS="-Wall -Werror $RPM_OPT_FLAGS $RPM_LD_FLAGS $ARCH_OPT_FLAGS"
	cachefilesd/cachefilesd.spec:   CFLAGS="-Wall $RPM_OPT_FLAGS -Werror"
	capstone/capstone.spec:V=1 CFLAGS="%{optflags}" \
	capstone/capstone.spec:%make_build PYTHON2=%{__python3} PYTHON3=%{__python3} CFLAGS="%{optflags}" # %{?_smp_mflags} parallel seems broken
	capstone/capstone.spec:%make_build PYTHON2=%{__python2} PYTHON3=%{__python2} CFLAGS="%{optflags}" # %{?_smp_mflags} parallel seems broken
	cdrkit/cdrkit.spec:export CFLAGS="$RPM_OPT_FLAGS -Wno-error=format-security -fno-strict-aliasing"
	ceph/ceph.spec:export CFLAGS="$RPM_OPT_FLAGS"
	ceph/ceph.spec:- Add CFLAGS=-DAO_USE_PTHREAD_DEFS on ARMv5tel
	ck/ck.spec:export CFLAGS="%{optflags}"
	cmake/cmake.spec:CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
	cogl/cogl.spec:CFLAGS="$RPM_OPT_FLAGS -fPIC"
	compface/compface.spec:CFLAGS="$RPM_OPT_FLAGS -fPIC" %configure
	conntrack-tools/conntrack-tools.spec:CFLAGS="${CFLAGS} -Wl,-z,lazy"
	coreutils/coreutils.spec:export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fpic"
	coreutils/coreutils.spec:CFLAGS="$CFLAGS -fno-lto"
	coreutils/coreutils.spec:CFLAGS="$CFLAGS -Dlint"
	cpio/cpio.spec:export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -pedantic -fno-strict-aliasing -Wall $CFLAGS"
	cpuid/cpuid.spec:make %{?_smp_mflags} CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64 -DVERSION=%{version}" LDFLAGS="$RPM_LD_FLAGS"
	crash/crash.spec:make RPMPKG="%{version}-%{release}" CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"
	cups/cups.spec:export CFLAGS="$RPM_OPT_FLAGS -fstack-protector-all -DLDAP_DEPRECATED=1"

### LDFLAGS in spec

	wfg /c/fedora% gr LDFLAGS c*/*.spec
	cdparanoia/cdparanoia.spec:make OPT="$RPM_OPT_FLAGS -Wno-pointer-sign -Wno-unused" LDFLAGS="%{?__global_ldflags}"
	cdparanoia/cdparanoia.spec:- Fix LDFLAGS propagation
	ceph/ceph.spec:export LDFLAGS="$RPM_LD_FLAGS"
	ceph/ceph.spec:- Add LDFLAGS=-lpthread on any ARM architecture
	cfitsio/cfitsio.spec:- Patch to use LDFLAGS (fixes bz #1547590)
	cgit/cgit.spec:LDFLAGS = %{build_ldflags}
	cgit/cgit.spec:LDFLAGS = %{build_ldflags}
	checkpolicy/checkpolicy.spec:- Use LDFLAGS from redhat-rpm-config
	chkconfig/chkconfig.spec:%make_build RPM_OPT_FLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"
	chkconfig/chkconfig.spec:- fix wrongly behaving LDFLAGS
	chkconfig/chkconfig.spec:- don't completely override LDFLAGS
	clamav/clamav.spec:export LDFLAGS=$(echo %{?__global_ldflags} | sed '/-Wl,--as-needed/!s/$/ -Wl,--as-needed/')

## global macros in code

	/c/rpm-software-management/rpm/build/build.c
	doScript()
	    case RPMBUILD_BUILD:
		mTemplate = "%{__spec_build_template}";
		mPost = "%{__spec_build_post}";
		mCmd = "%{__spec_build_cmd}";
		break;
	    default:
		mTemplate = "%{___build_template}";
		mPost = "%{___build_post}";
		mCmd = "%{___build_cmd}";
		break;

	/c/rpm-software-management/rpm/macros.in
	%__spec_build_pre       %{___build_pre}

	%__spec_build_template  #!%{__spec_build_shell}\
	%{__spec_build_pre}\
	%{nil}

	%___build_template      #!%{___build_shell}\
	%{___build_pre}\
	%{nil}

	# C compiler flags.  This is traditionally called CFLAGS in makefiles.
	# Historically also available as %%{optflags}, and %%build sets the
	# environment variable RPM_OPT_FLAGS to this value.
	%build_cflags %{optflags}

	# C++ compiler flags.  This is traditionally called CXXFLAGS in makefiles.
	%build_cxxflags %{optflags}

	# Expands to shell code to seot the compiler/linker environment
	# variables CFLAGS, CXXFLAGS, FFLAGS, FCFLAGS, LDFLAGS if they have
	# not been set already.
	%set_build_flags \
	  CFLAGS="${CFLAGS:-%{?build_cflags}}" ; export CFLAGS ; \
	  CXXFLAGS="${CXXFLAGS:-%{?build_cxxflags}}" ; export CXXFLAGS ; \
	  FFLAGS="${FFLAGS:-%{?build_fflags}}" ; export FFLAGS ; \
	  FCFLAGS="${FCFLAGS:-%{?build_fflags}}" ; export FCFLAGS ; \
	  LDFLAGS="${LDFLAGS:-%{?build_ldflags}}" ; export LDFLAGS

	# The configure macro runs autoconf configure script with platform specific
	# directory structure (--prefix, --libdir etc) and compiler flags
	# such as CFLAGS.
	#
	%_configure ./configure
	%configure \
	  %{set_build_flags}; \
	  %{_configure} --host=%{_host} --build=%{_build} \\\
		--program-prefix=%{?_program_prefix} \\\
		--disable-dependency-tracking \\\
		--prefix=%{_prefix} \\\

## global macros in real env

	$ rpm --showrc

	RPMRC VALUES:
	archcolor             : 2
	optflags              : %{__global_compiler_flags} -fasynchronous-unwind-tables -fstack-clash-protection

	-13: __global_compiler_flags    -O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstgcc-switches %{_hardened_cflags}

	-13: __cc       gcc
	-13: __cpp      gcc -E
	-13: __cxx      g++

	-13: ___build_pre
	  RPM_SOURCE_DIR="%{u2p:%{_sourcedir}}"
	  RPM_BUILD_DIR="%{u2p:%{_builddir}}"
	  RPM_OPT_FLAGS="%{optflags}"
	  RPM_LD_FLAGS="%{?build_ldflags}"
	  RPM_ARCH="%{_arch}"
	  RPM_OS="%{_os}"
	  RPM_BUILD_NCPUS="%{_smp_build_ncpus}"
	  export RPM_SOURCE_DIR RPM_BUILD_DIR RPM_OPT_FLAGS RPM_ARCH RPM_OS RPM_BUILD_NCPUS RPM_OPT_FLAGS

	-13: build_cflags       %{optflags}
	-13: build_cxxflags     %{optflags}
	-13: build_fflags       %{optflags} -I%{_fmoddir}
	-13: build_ldflags      -Wl,-z,relro %{_ld_as_needed_flags} %{_ld_symbols_flags} %{_hardened_ldflags}

	-13: cmake
	  CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
	  CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
	  FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ;
	  FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ;
	  %{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;}
	  %__cmake \
		-DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \
		-DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \
		-DCMAKE_Fortran_FLAGS_RELEASE:STRING="-DNDEBUG" \
		-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
		-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
		-DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
		-DLIB_INSTALL_DIR:PATH=%{_libdir} \
		-DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
		-DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
	%if "%{?_lib}" == "lib64"
		%{?_cmake_lib_suffix64} \
	%endif
		-DBUILD_SHARED_LIBS:BOOL=ON

	-13: py3_build  %{expand:\
	  CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}"\
	  %{__python3} %{py_setup} %{?py_setup_args} build --executable="%{__python3} %{py3_shbang_opts}" %{?*}
	  sleep 1
	}
