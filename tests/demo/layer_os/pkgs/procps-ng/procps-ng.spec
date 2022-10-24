Name: 		procps-ng
Version: 	3.3.17
Release:	2
Summary: 	Utilities that provide system information.
License: 	GPL+ and GPLv2 and GPLv2+ and GPLv3+ and LGPLv2+
URL: 		https://sourceforge.net/projects/procps-ng/

Source0: 	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
Source1: 	README.md
Source2: 	README.top

Patch1: 	0001-top-fix-two-potential-alternate-display-mode-abends.patch
Patch2: 	0002-top-In-the-bye_bye-function-replace-fputs-with-the-w.patch
Patch3: 	0003-add-options-M-and-N-for-top.patch
Patch4: 	0004-top-exit-with-error-when-pid-overflow.patch
Patch5:		0005-fix-a-fix-for-the-bye_bye-function.patch

BuildRequires: 	ncurses-devel libtool autoconf automake gcc gettext-devel systemd-devel

Provides: 	procps = %{version}-%{release}
Provides: 	%{name}	

%description
The procps package contains a set of system utilities that provide
system information. Procps includes ps, free, skill, pkill, pgrep,
snice, tload, top, uptime, vmstat, pidof, pmap, slabtop, w, watch
and pwdx.

%package 	devel
Summary:  	The devel for %{name} 
Requires: 	%{name} = %{version}-%{release}
Provides: 	procps-devel = %{version}-%{release}

%description 	devel
System and process monitoring utilities

%package 	i18n
Summary:  	Internationalization pack for %{name} 
Requires: 	%{name} = %{version}-%{release}
BuildArch: 	noarch

%description 	i18n
The package is used for the Internationalization of %{name}

%package_help

%prep
%autosetup -n procps-%{version} -p1

cp -p %{SOURCE1} .
cp -p %{SOURCE2} top/

%build
autoreconf -ivf

%configure  --exec-prefix=/ --docdir=/unwanted --disable-w-from --disable-kill --enable-watch8bit \
           --enable-skill --enable-sigwinch --enable-libselinux --with-systemd --disable-modern-top

make CFLAGS="%{optflags}"

%install
%make_install

%find_lang %{name} --all-name --with-man

ln -s %{_bindir}/pidof %{buildroot}%{_sbindir}/pidof

%ldconfig_scriptlets

%files
%doc COPYING COPYING.LIB
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB
%{_libdir}/libprocps.so.*
%{_bindir}/*
%{_sbindir}/*
%exclude %{_libdir}/libprocps.la
%exclude /unwanted/*
%exclude %{_libdir}/*.a

%files devel
%doc COPYING COPYING.LIB
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB
%{_libdir}/libprocps.so
%{_libdir}/pkgconfig/libprocps.pc
%{_includedir}/proc

%files i18n -f %{name}.lang

%files help
%doc AUTHORS Documentation/bugs.md Documentation/FAQ NEWS README.md top/README.top Documentation/TODO
%{_mandir}/man*

%changelog
* Sat Jan 29 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 3.3.17-2
- fix file type chamges caused by top -b redirection

* Thu Dec 2 2021 zhouwenpei <zhouwenpei1@huawei.com> - 3.3.17-1
- update to 3.3.17

* Wed Jun 30 2021 hewenliang <hewenliang4@huawei.com> - 3.3.16-16
- sync patches

* Sat Feb 27 2021 hewenliang <hewenliang4@huawei.com> - 3.3.16-15
- sync patches

* Sat Feb 27 2021 hewenliang <hewenliang4@huawei.com> - 3.3.16-14
- sync patches

* Tue Nov 03 2020 xinghe <xinghe1@huawei.com> - 3.3.16-13
- sync patchs

* Wed Sep 23 2020 MarsChan <chenmingmin@huawei.com> - 3.3.16-12
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:A kernel change means we cannot trust what sysconf(SC_ARG_MAX)
       returns. We clamp it so its more than 4096 and less than 128*1024
       which is what findutils does.

* Tue Jan 7 2020 MarsChan <chenmingmin@huawei.com> - 3.3.16-11
- Type:upgrade
- ID:NA
- SUG:NA
- DESC: upgrade to version 3.3.16 and delete the patch between
        3.3.15 and 3.3.16.

* Mon Dec 23 2019 wangshuo <wangshuo47@huawei.com> - 3.3.15-10
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: add liscense to main and devel package.

* Thu Dec 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.3.15-9
- Fix typo

* Fri Mar 15 2019 xuwei<xuwei58@huawei.com> - 3.3.15-8
- Type:bugfix
- ID:NA
- SUG:restart
- DEC:top: don't mess with groff line length in man document
      top: add another field sanity check in 'config_file()'
      top: prevent buffer overruns in 'inspection_utility()'
      docs: Tidying of ps,kill and skill manpages
      library: avoid problems involving 'supgid' mishandling
      w: Prevent out-of-bounds reads in
      w: Clamp maxcmd to the MIN/MAX_CMD_WIDTH range.
      vmstat: getopt*() returns -1 when done, not EOF.
      vmstat: Replace memcmp() with strncmp().
      vmstat: Check return values of localtime() and
      vmstat: Prevent out-of-bounds writes in new_header()
      top: the '#define PRETEND2_5_X' was found to be broken
      procio: use the user-supplied delimiter to split large
      procio: fix potential out-of-bounds access when write
      sysctl: do not report set key in case `close_stream`

* Tue Jan 29 2019 huangchangyu<huangchangyu@huawei.com> - 3.3.15-7
- Type:bugfix
- ID:NA
- SUG:NA
- DEC:sync patches

* Wed Jan 23 2019 xuchunmei<xuchunmei@huawei.com> - 3.3.15-6
- Type:bugfix
- ID:NA
- SUG:restart
- DEC:top exit with error when pid overflow

* Fri Jan 11 2019 xuchunmei<xuchunmei@huawei.com> - 3.3.15-5
- Type:feature
- ID:NA
- SUG:restart
- DEC:add options -M and -N for top

* Sat Jul 18 2018 openEuler Buildteam <buildteam@openeuler.org> - 3.3.15-4
- Package init
