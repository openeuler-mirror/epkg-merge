Name:     bash
Version:  5.1.8
Release:  4
Summary:  It is the Bourne Again Shell
License:  GPLv3
URL:      https://www.gnu.org/software/bash
Source0:  https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

Source1: dot-bashrc
Source2: dot-bash_profile
Source3: dot-bash_logout

# PATCH-FIX-UPSTREAM

Patch115: bash-2.05a-interpreter.patch
Patch118: bash-2.05b-pgrp_sync.patch
Patch125: bash-4.0-nobits.patch
Patch129: bash-4.2-coverity.patch
# rh1102815
Patch133: bash-4.3-noecho.patch
# fix bash leaks memory when LC_ALL set-rh1241533,rh1224855
Patch134: bash-4.3-memleak-lc_all.patch
Patch137: bugfix-Forbidden-non-root-user-to-clear-history.patch
Patch138: enable-dot-logout-and-source-bashrc-through-ssh.patch
Patch139: cd-alias.patch
Patch140: bash-5.1-sw.patch

BuildRequires: gcc bison texinfo autoconf ncurses-devel
# Required for bash tests
BuildRequires: glibc-all-langpacks

Requires:      filesystem

Provides:      /bin/sh /bin/bash

%description
Bash is the GNU Project's shell. Bash is the Bourne Again SHell. Bash is an sh-compatible
shell that incorporates useful features from the Korn shell (ksh) and C shell (csh). It is
intended to conform to the IEEE POSIX P1003.2/ISO 9945.2 Shell and Tools standard. It offers
functional improvements over sh for both programming and interactive use. In addition, most
sh scripts can be run by Bash without modification.

%package devel
Summary: Development headers for %{name}
Requires: %{name} = %{version}-%{release}
Requires: pkgconf-pkg-config

%description devel
This package contains development files for %{name}.

%package        help
Summary:        Documents for %{name}
Buildarch:      noarch
Requires:	man info
Provides:       %{name}-doc = %{version}-%{release}
Obsoletes:      %{name}-doc < %{version}-%{release}

%description help
Man pages and other related documents for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoconf
%configure --with-bash-malloc=no --with-afs
MFLAGS="CPPFLAGS=-D_GNU_SOURCE -DRECYCLES_PIDS -DDEFAULT_PATH_VALUE='\"/usr/local/bin:/usr/bin\"' `getconf LFS_CFLAGS`"
make "$MFLAGS" version.h
make "$MFLAGS" -C builtins
%make_build "$MFLAGS"

%install
%make_install install-headers
ln -sf bash %{buildroot}%{_bindir}/sh
install -pDm 644 %SOURCE1 %{buildroot}/etc/skel/.bashrc
install -pDm 644 %SOURCE2 %{buildroot}/etc/skel/.bash_profile
install -pDm 644 %SOURCE3 %{buildroot}/etc/skel/.bash_logout
install -pDm 644 ./configs/alias.sh %{buildroot}%{_sysconfdir}/profile.d/alias.sh

# bug #820192, need to add execable alternatives for regular built-ins
for ea in alias bg cd command fc fg getopts hash jobs read type ulimit umask unalias wait
do
  cat <<EOF > "%{buildroot}"/%{_bindir}/"$ea"
#!/bin/sh
builtin $ea "\$@"
EOF
chmod +x "%{buildroot}"/%{_bindir}/"$ea"
done

%find_lang %{name}

%check
make check

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) /etc/skel/.b*
%{_bindir}/{sh,bash,alias,bg,cd,command,fc,fg,wait,bashbug}
%{_bindir}/{hash,getopts,jobs,read,type,ulimit,umask,unalias}
%config(noreplace) %{_sysconfdir}/profile.d/alias.sh

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
%{_libdir}/bash/*
%exclude %{_libdir}/bash/Makefile*

%files help
%defattr(-,root,root)
%doc NOTES
%doc doc/*.ps doc/*.0 doc/*.html doc/*.txt
%doc %{_docdir}/%{name}/*
%{_infodir}/%{name}.info*
%{_mandir}/man1/*.gz
%exclude %{_infodir}/dir

%changelog
* Mon Aug 15 2022 panxiaohe <panxh.life@foxmail.com> - 5.1.8-4
- fix bugfix-Forbidden-non-root-user-to-clear-history.patch

* Wed Jul 20 2022 wuzx<wuzx1226@qq.com> - 5.1.8-3
- add sw64 patch

* Wed Jul 6 2022 zoulin <zoulin13@h-partners.com> - 5.1.8-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: add alias.sh

* Thu Dec 30 2021 wangjie <wangjie375@huawei.com> - 5.1.8-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: Update bash to 5.1.8

* Fri Jun 18 2021 liujian<liujianliu.liu@huawei.com> - 5.1-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add upstream patches

* Mon May 31 2021 liujian<liujianliu.liu@huawei.com> - 5.1-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:upgrade to 5.1

* Tue Mar 30 2021 shenyangyang<shenyangyang4@huawei.com> - 5.0-17
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Rebuild for openEuler-rpm-config moving /usr/lib/rpm/openEuler/xxxx
       to /usr/lib/xxxx

* Wed Jan 6 2021 Liquor <lirui130@huawei.com> - 5.0-16
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify file /etc/skel/.b* permissions to 644

* Sat Oct 31 2020 Liquor <lirui130@huawei.com> - 5.0-15
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix format error

* Thu Apr 30 2020 licihua <licihua@huawei.com> - 5.0-14
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add upstream patch

* Wed Apr 8 2020 openEuler Buildteam <licihua@huawei.com> - 5.0-13
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add upstream patches

* Thu Mar 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0-12
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:remove comment in dot-bash_profile

* Tue Mar 10 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0-11
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add build requires of ncurses-devel

* Fri Feb 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0-10
- Type:CVE
- ID:NA
- SUG:NA
- DESC:CVE-2019-18276

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0-9
- resolve compile problems.

* Mon Jan 6 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0-8
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:delete redundant files

* Wed Dec 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.0-7
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add provides of bash-doc

* Thu Oct 24 2019 shenyangyang<shenyangyang4@huawei.com> - 5.0-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add build requires of bison and texinfo

* Fri Oct 11 2019 shenyangyang<shenyangyang4@huawei.com> - 5.0-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:move the man files

* Mon Sep 30 2019 shenyangyang<shenyangyang4@huawei.com> - 5.0-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify requires

* Sat Sep 21 2019 shenyangyang<shenyangyang4@huawei.com> - 5.0-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:revise description

* Wed Sep 4 2019 shenyangyang<shenyangyang4@huawei.com> - 5.0-2
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:remove man to main package

* Mon Sep 2 2019 shenyangyang<shenyangyang4@huawei.com> - 5.0-1
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:strenthen spec

* Sat Mar 16 2019 hanzhijun<hanzhijun1@huawei.com> - 4.4.23-7
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix pathname expansion of directory

* Fri Jan 25 2019 Xiaoqi Guo<guoxiaoqi2@huawei.com> - 4.4.23-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:1000 Forbidden non root user to clear history

* Mon Oct 08 2018 licunlong <licunlong@huawei.com> - 4.4.23-5
- Package Initialization
