## rpmEnv 字段：映射/传递 build options 到 spec

在包YAML中增加rpmEnv小节，其中的key/val会被视为rpm macro，进而合入生成的spec文件。
其作用类似env环境变量，用于定制RPM spec。

	rpmEnv:
		macroName: macro value

在各个包名字空间下的rpmEnv，加到所生成spec的头部。
rpmEnv尽量不暴露给用户或者第三方定制。避免在YAML字段中引用rpmEnv字段下的值。相反，rpmEnv可以引用其它字段。

数据流方向如下：

	customizable YAML fields
	=> pkgs.<pkg>.rpmEnv 	=> spec header macro definitions

## compiler cflags 定制

	rpmEnv:
		__cc: %%{env.compiler}
		build_cflags: %%{env.cflags}
		build_cxxflags: %%{env.cxxflags}

## reference: 定制相关 rpm macros

	$ rpm --showrc

	-13: __cc       gcc
	-13: __cpp      gcc -E
	-13: __cxx      g++

	-13: set_build_flags    
	  CFLAGS="${CFLAGS:-%{build_cflags}}" ; export CFLAGS ; 
	  CXXFLAGS="${CXXFLAGS:-%{build_cxxflags}}" ; export CXXFLAGS ; 
	  FFLAGS="${FFLAGS:-%{build_fflags}}" ; export FFLAGS ; 
	  FCFLAGS="${FCFLAGS:-%{build_fflags}}" ; export FCFLAGS ; 
	  LDFLAGS="${LDFLAGS:-%{build_ldflags}}" ; export LDFLAGS

	-13: configure  
	  %{set_build_flags}; 
	  [ "%_configure_gnuconfig_hack" = 1 ] && for i in $(find $(dirname %{_configure}) -name config.guess -o -name config.sub) ; do 
	      [ -f /usr/lib/rpm/openEuler/$(basename $i) ] && %{__rm} -f $i && %{__cp} -fv /usr/lib/rpm/openEuler/$(basename $i) $i ; 
	  done ; 
	  [ "%_configure_libtool_hardening_hack" = 1 ] && [ x != "x%{_hardened_ldflags}" ] && 
	      for i in $(find . -name ltmain.sh) ; do 
		%{__sed} -i.backup -e 's~compiler_flags=$~compiler_flags="%{_hardened_ldflags}"~' $i 
	      done ; 
	  %{_configure} --build=%{_build} --host=%{_host} \
		--program-prefix=%{?_program_prefix} \
		--disable-dependency-tracking \
		%{?_configure_disable_silent_rules:--disable-silent-rules} \
		--prefix=%{_prefix} \
		--exec-prefix=%{_exec_prefix} \
		--bindir=%{_bindir} \
		--sbindir=%{_sbindir} \
		--sysconfdir=%{_sysconfdir} \
		--datadir=%{_datadir} \
		--includedir=%{_includedir} \
		--libdir=%{_libdir} \
		--libexecdir=%{_libexecdir} \
		--localstatedir=%{_localstatedir} \
		--sharedstatedir=%{_sharedstatedir} \
		--mandir=%{_mandir} \
		--infodir=%{_infodir}


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

