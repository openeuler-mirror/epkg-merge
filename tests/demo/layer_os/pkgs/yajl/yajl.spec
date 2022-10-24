Name:           yajl
Version:        2.1.0
Release:        19
Summary:        Yet Another JSON Library
License:        ISC
URL:            https://github.com/lloyd/yajl
Source0:        https://github.com/lloyd/yajl/archive/%{version}.tar.gz

Patch1:         0001-yajl-2.1.0-pkgconfig-location.patch
Patch2:         0002-yajl-2.1.0-pkgconfig-includedir.patch
Patch3:         0003-yajl-2.1.0-test-location.patch
Patch4:         0004-yajl-2.1.0-dynlink-binaries.patch
Patch5:         0005-yajl-2.1.0-fix-memory-leak.patch
Patch6:         0006-fix-memory-leak-of-ctx-root.patch
Patch7:         0007-add-cmake-option-for-test-and-binary.patch
Patch8:         backport-CVE-2022-24795.patch
Patch9:         yajl-assert-error-when-memory-allocation-failed.patch

BuildRequires:  cmake gcc

%description
yajl is a small event-driven JSON parser written in ANSI C, and a small
validating JSON generator.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package provides the libraries and includes
necessary for developing against the yajl library.

%prep
%autosetup -n %{name}-%{version} -p1

%build
mkdir build
cd build
%cmake ..
%make_build VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
cd build
%make_install

%check
cd test/parsing
./run_tests.sh
cd ../api
./run_tests.sh

%files
%defattr(-,root,root)
%doc COPYING README ChangeLog TODO
%{_bindir}/json_reformat
%{_bindir}/json_verify

%{_libdir}/libyajl.so.*
%{_libdir}/libyajl.so

%files devel
%dir %{_includedir}/yajl
%{_includedir}/yajl/yajl_common.h
%{_includedir}/yajl/yajl_gen.h
%{_includedir}/yajl/yajl_parse.h
%{_includedir}/yajl/yajl_tree.h
%{_includedir}/yajl/yajl_version.h

%{_libdir}/pkgconfig/yajl.pc
%{_libdir}/libyajl_s.a

%changelog
* Thu Sep 22 2022 panxiaohe <panxh.life@foxmail.com> - 2.1.0-19
- modify URL

* Fri Sep 9 2022 panxiaohe <panxh.life@foxmail.com> - 2.1.0-18
- assert error when memory allocation failed

* Fri Sep 9 2022 panxiaohe <panxh.life@foxmail.com> - 2.1.0-17
- fix CVE-2022-24795

* Wed Jun 8 2022 haozi007 <liuhao27@h-partners.com> - 2.1.0-16
- add index for patch and add cmake options

* Sat Feb 12 2022 fuanan <fuanan3@h-partners.com> - 2.1.0-15
- fix memory leaks in yajl_tree_parse

* Tue Jun 8 2021 panxiaohe<panxiaohe@huawei.com> - 2.1.0-14
- add gcc to BuildRequires

* Wed Sep 9 2020 wangchen<wangchen137@huawei.com> - 2.1.0-13
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify the URL of Source0

* Sat Aug 31 2019 dongjian<dongjian13@huawei.com> - 2.1.0-12
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: modify summary and some structures

* Tue Aug 20 2019 fangyufa<fangyufa1@huawei.com> - 2.1.0-11.h3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: modify name of patch

* Fri Aug 09 2019 fangyufa<fangyufa1@huawei.com> - 2.1.0-11.h2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: add head info of patch

* Thu Aug 01 2019 shenyangyang <shenyangyang4@huawei.com> - 2.1.0-11.h1
- Package Initialization
