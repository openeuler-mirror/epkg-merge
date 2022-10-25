%define Rversion %(echo %{version} | sed -e 's/\\./_/g' -e 's/^/R_/')
Name:           expat
Version:        2.4.8
Release:        3
Summary:        An XML parser library
License:        MIT
URL:            https://libexpat.github.io/
Source0:        https://github.com/libexpat/libexpat/releases/download/%{Rversion}/expat-%{version}.tar.gz

Patch0:         backport-0001-CVE-2022-40674.patch
Patch1:         backport-0002-CVE-2022-40674.patch

BuildRequires:  sed,autoconf,automake,gcc-c++,libtool,xmlto

%description
expat is a stream-oriented XML parser library written in C.
expat excels with files too large to fit RAM, and where
performance and flexibility are crucial.

%package devel
Summary:        Development files
Requires:       %{name} = %{version}-%{release}
%description devel
This package provides with static libraries and  header files for developing with expat.

%package_help

%prep
%autosetup -p1

autoreconf -fiv
%build
%configure CFLAGS="$RPM_OPT_FLAGS -fPIC" DOCBOOK_TO_MAN="xmlto man --skip-validation"
%make_build

%install
%makeinstall
find %{buildroot} -type f -name changelog -delete

%check
make check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING AUTHORS
%{_bindir}/*
%{_libdir}/libexpat.so.1*
%exclude %{_docdir}/%{name}/AUTHORS

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/{libexpat.*a,libexpat.so}
%{_libdir}/cmake/expat-%{version}
%{_libdir}/pkgconfig/expat.pc

%files help
%defattr(-,root,root)
%doc README.md
%{_mandir}/man1/*

%changelog
* Thu Sep 15 2022 panxiaohe <panxh.life@foxmail.com> - 2.4.8-3
- add test for CVE-2022-40674

* Thu Sep 15 2022 dillon chen<dillon.chen@gmail.com> -2.4.8-2
- fix CVE-2022-40674

* Fri Jul 1 2022 panxiaohe <panxh.life@foxmail.com> - 2.4.8-1
- update to 2.4.8

* Mon Mar 7 2022 yangzhuangzhuang <yangzhuangzhuang1@h-partners.com> - 2.4.6-2
- Relax fix to CVE-2022-25236

* Sat Feb 26 2022 yangzhuangzhuang <yangzhuangzhuang1@h-partners.com> - 2.4.6-1
- update to 2.4.6
- fix CVE-2022-25235 CVE-2022-25236 CVE-2022-25313 CVE-2022-25314 CVE-2022-25315

* Mon Feb 7 2022 yangzhuangzhuang <yangzhuangzhuang1@h-partners.com> - 2.4.4-1
- update to 2.4.4
- fix CVE-2022-23852 CVE-2022-23990

* Mon Jan 17 2022 wangjie <wangjie375@huawei.com> - 2.4.1-2
- Type:CVE
- ID:CVE-2021-45960 CVE-2021-46143 CVE-2022-22822 CVE-2022-22823 CVE-2022-22824 CVE-2022-22825 CVE-2022-22826 CVE-2022-22827
- SUG:NA
- DESC:fix CVE-2021-45960 CVE-2021-46143
       CVE-2022-22822 CVE-2022-22823 CVE-2022-22824 CVE-2022-22825 CVE-2022-22826 CVE-2022-22827

* Tue Jul 6 2021 panxiaohe <panxiaohe@huawei.com> - 2.4.1-1
- update to 2.4.1
- fix CVE-2013-0340

* Wed Jan 20 2021 wangchen <wangchen137@huawei.com> - 2.2.10-1
- update to 2.2.10

* Sun Jun 28 2020 liuchenguang <liuchenguang4@huawei.com> - 2.2.9-2
- quality enhancement synchronization github patch

* Mon May 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.2.9-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update to 2.2.9

* Mon Oct 21 2019 shenyangyang <shenyangyang4@huawei.com> - 2.2.6-5
- Type:NA
- ID:NA
- SUG:NA
- DESC:modify the directory of AUTHORS

* Mon Oct 21 2019 shenyangyang <shenyangyang4@huawei.com> - 2.2.6-4
- Type:NA
- ID:NA
- SUG:NA
- DESC:move AUTHORS to license directory

* Sat Sep 28 2019 shenyangyang<shenyangyang4@huawei.com> - 2.2.6-3
- Type:cves
- ID:CVE-2019-15903
- SUG:NA
- DESC:fix CVE-2019-15903

* Fri Aug 30 2019 gulining<gulining1@huawei.com> - 2.2.6-2
- Type:cves
- ID:CVE-2018-20843
- SUG:NA
- DESC:fix CVE-2018-20843

* Thu Aug 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.2.6-1
- Package Init
