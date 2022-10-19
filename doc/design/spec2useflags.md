# spec2yaml中新增python逻辑对%configure块进行解析

- 扫描其中的--enable-xxx --disable-xxx --with-xxx --without-xxx
- 取出其中的固定选项，存入 YAML env.configureFlags，然后用%%{env.configureFlags}替代之
- 受with macro控制的条件选项，安排YAML对应的useConfigureFlag，并定义传入macro

	useConfigureFlags:
		$flag:
	rpmEnv:
		_with_$flag    when +$flag: 1	# for bcond_with
		_without_$flag when -$flag: 1	# for bcond_without

Q: shall we define %_with_$flag/%_without_$flag or %with_$flag?

rpmEnv里的宏定义，会被yaml2spec加到spec的最前面。此处定义_with_$flag，可以起到执行 rpmbuild --with-$flag 的效果。

- 受%define/%global macro控制的条件选项，安排YAML对应的useFlag，并定义传入macro

	useFlags:
		$flag:
	rpmMacros:
		- "%define $flag %%{use.$flag}"

此处需要把rpmMacros下原来的那行%define/%global替换掉。
未来也可以考虑抽取到rpmEnv，把可定制项往rpmEnv集中。

# 示例

spec input:

	%global build_pdf_doc 0 	# 为简单起见，只处理没有被其它%if条件包围的情况

	%configure --disable-static \
	%if %{build_pdf_doc}
		   --enable-doxygen-pdf \
	%else
		   --disable-doxygen-pdf \
	%endif
		   --disable-doxygen-ps \
		   --enable-doxygen-html \
		   --enable-examples

yaml output:

	phase.build:
		%configure %%{env.configureFlags} \
		%if %{build_pdf_doc}
			   --enable-doxygen-pdf \
		%else
			   --disable-doxygen-pdf \
		%endif
	env.configureFlags: |
			--disable-static 
			--disable-doxygen-ps 
			--enable-doxygen-html 
			--enable-examples
	useFlags:
		build_pdf_doc:
			default: false
	rpmMacros:
		# 替换掉原来的 - %global build_pdf_doc 0
		- "%global build_pdf_doc %%{use.build_pdf_doc}"

Notes: spec 里
		%if %{build_pdf_doc}
除了控制%configureFlags，可能还会控制别的代码块。为简单起见，保留之，暂不移入YAML，只是在YAML里创建对应的use定制选项。

# 在YAML里引用/展开简单的 RPM macro

	rpmMacros:
	    - "%global debuginfodir /usr/lib/debug"
	    - "%global upstream_version    5.10"
	    - "%global upstream_sublevel   0"
	    - "%global devel_release       104"
	    - "%global maintenance_release .0.0"
	    - "%global pkg_release         .54"

We can move the above "%global var fixed-value" lines to

	rpmEnv:
	  debuginfodir:         "/usr/lib/debug"
	  upstream_version:     "5.10"
	  upstream_sublevel:    "0"
	  devel_release:        "104"
	  maintenance_release:  ".0.0"
	  pkg_release:          ".54"

Then we'll be able to expand %{} in YAML like this

	%{xxx}
=>
	%%{rpmEnv.xxx}

For example,

spec file

	%global pcs_snmp_pkg_name  pcs-snmp
	%package -n %{pcs_snmp_pkg_name}
	%post -n %{pcs_snmp_pkg_name}
	%systemd_post pcs_snmp_agent.service

to YAML file

	rpmEnv:
	  pcs_snmp_pkg_name:  pcs-snmp
	subpackage:
	  %{pcs_snmp_pkg_name}:
	    runtimePhase.post:
	      %systemd_post pcs_snmp_agent.service

The macro in the above key can be expanded as follows

  %{pcs_snmp_pkg_name}
  =>
  %%{rpmEnv.pcs_snmp_pkg_name}
  =>
  pcs-snmp

The macro in key shall be expanded before adding to config space.

# reference: %configure examples in real spec:

	%configure --enable-systemd=yes

	%configure --with-modules --disable-static --with-gnutls --without-openssl --with-debug

	%configure --disable-silent-rules --disable-zip-archive --disable-static

	%configure --disable-static \
	%if %{build_pdf_doc}
		   --enable-doxygen-pdf \
	%else
		   --disable-doxygen-pdf \
	%endif
		   --disable-doxygen-ps \
		   --enable-doxygen-html \
		   --enable-examples

	%configure %{?configure_opts}

	%configure --disable-static --enable-pulse --enable-alsa --enable-null --disable-oss --with-builtin=dso --with-systemdsystemunitdir=/usr/lib/systemd/system

# reference: rpm code

/c/rpm-software-management/rpm/rpmpopt.in

	rpmbuild alias --with           --define "_with_!#:+     --with-!#:+" \
		--POPTdesc=$"enable configure <option> for build" \
		--POPTargs=$"<option>"
	rpmbuild alias --without        --define "_without_!#:+  --without-!#:+" \
		--POPTdesc=$"disable configure <option> for build" \
		--POPTargs=$"<option>"

/c/rpm-software-management/rpm/macros.in

	#
	# The bottom line: never use without_foo, _with_foo nor _without_foo, only
	# with_foo. This way changing default set of bconds for given spec is just
	# a matter of changing single line in it and syntax is more readable.
	%bcond_with()           %{expand:%%{?_with_%{1}:%%global with_%{1} 1}}
	%bcond_without()        %{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}

/c/rpm-software-management/rpm/macros.in

	# Shorthand for %{defined with_...}
	%with()         %{expand:%%{?with_%{1}:1}%%{!?with_%{1}:0}}
	%without()      %{expand:%%{?with_%{1}:0}%%{!?with_%{1}:1}}

