
Name:           libaio
Version:        0.3.112
Release:        5
Summary:        Linux-native asynchronous I/O access library
License:        LGPLv2+
URL:            https://pagure.io/libaio
Source:         https://releases.pagure.org/libaio/libaio-%{version}.tar.gz

Patch0:         0000-libaio-install-to-destdir-slash-usr.patch
Patch1:         0001-libaio-arm64-ilp32.patch
%ifarch aarch64 aarch64_ilp32 x86_64
Patch2:         0002-libaio-makefile-cflags.patch
%endif
Patch3:         0003-libaio-fix-for-x32.patch
Patch4:         0004-libaio-makefile-add-D_FORTIFY_SOURCE-flag.patch
Patch5:         0005-Fix-compile-error-that-exec-checking-need-super-priv.patch

BuildRequires:  gcc

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package  devel
Summary:  Files for libaio development
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for libaio development

%prep
%setup -q -a 0
%patch0   -p1 -b .install-to-destdir-slash-usr
%patch1   -p1 -b .arm64-ilp32
%ifarch aarch64 aarch64_ilp32 x86_64
%patch2   -p1 -b .makefile-cflags
%endif
%patch3   -p1 -b .fix-x32
%patch4   -p1 -b .makefile-add-D_FORTIFY_SOURCE-flag
%patch5   -p1 -b .fix-compile-error

mv %{name}-%{version} setup-%{name}-%{version}

%build
make -C setup-%{name}-%{version} soname='libaio.so.1.0.0' libname='libaio.so.1.0.0'
make

%install
pushd setup-%{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 \
  $RPM_BUILD_ROOT/%{_libdir}/libaio.so.1.0.0
popd
make destdir=$RPM_BUILD_ROOT prefix=/ libdir=/%{_lib} usrlibdir=%{_libdir} \
        includedir=%{_includedir} install

rm -rf %{buildroot}%{_usr}/%{_lib}/libaio.a

%ldconfig_scriptlets

%check
make check

%files
%license COPYING
%attr(0755,root,root) %{_libdir}/libaio.so.*

%files devel
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{_libdir}/libaio.so

%changelog
* Fri Jun 24 2022 lihaoxiang <lihaoxiang9@huawei.com> - 0.3.112-5
- fix compile error 

* Thu May 12 2022 Li Jinlin  <lijinlin3@huawei.com> - 0.3.112-4
- fix patch4 not apply

* Wed Dec 1 2021 volcanodragon <linfeilong@huawei.com> - 0.3.112-3
- add D_FORTIFY_SOURCE flag to Makefile for security

* Sun Sep 26 2021 Li Jinlin  <lijinlin3@huawei.com> - 0.3.112-2
- enable %check option

* Sat Jul 18 2020 volcanodragon <linfeilong@huawei.com> - 0.3.112-1
- update from 0.3.111 to 0.3.112

* Wed Jul 1 2020 Wu Bo <wubo009@163.com> - 0.3.111-6
- rebuild package

* Tue Mar 17 2020 hy-euler <eulerstoragemt@huawei.com> - 0.3.111-5
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:Add secure compilation options for x86_64.

* Wed Sep 4 2019 sunshihao<sunshihao@huawei.com> - 0.3.111-4
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:openEuler Debranding.

* Wed Aug 21 2019 wubo <wubo40@huawei.com> - 0.3.111-3.h4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change patch name

* Tue Apr 2 2019 guyue <guyue7@huawei.com> 0.3.111-3.h3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:delete useless code

* Thu Feb 14 2019 geruijun <geruijun@huawei.com> 0.3.111-3.h2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add backport patches

* Sat Jan 26 2019 wangxiao <wangxiao65@huawei.com> 0.3.111-h1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: support ilp32 for aarch64

- Package Init
