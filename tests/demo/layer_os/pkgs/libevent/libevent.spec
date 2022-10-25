Name:           libevent
Version:        2.1.12
Release:        6
Summary:        An event notification library

License:        BSD
URL:            http://libevent.org/
Source0:        https://github.com/libevent/libevent/releases/download/release-%{version}-stable/libevent-%{version}-stable.tar.gz

BuildRequires: gcc doxygen openssl-devel

Patch0: libevent-nonettests.patch
Patch1: http-add-callback-to-allow-server-to-decline-and-the.patch
Patch2: add-testcases-for-event.c-apis.patch

# Temporary downstream change: revert a problematic upstream change
# until Transmission is fixed. Please drop the patch when the Transmission
# issue is fixed.
# https://github.com/transmission/transmission/issues/1437
Patch3: 0001-Revert-Fix-checking-return-value-of-the-evdns_base_r.patch

%description
Libevent additionally provides a sophisticated framework for buffered network IO, with support for sockets,
filters, rate-limiting, SSL, zero-copy file transmission, and IOCP.
Libevent includes support for several useful protocols, including DNS, HTTP, and a minimal RPC framewor.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and libraries for developing
with %{name}.

%prep
%autosetup -n libevent-%{version}-stable -p1

%build
%configure --disable-dependency-tracking --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%ldconfig_scriptlets

%files
%doc ChangeLog
%license LICENSE
%{_libdir}/libevent-2.1.so.*
%{_libdir}/libevent_core-2.1.so.*
%{_libdir}/libevent_extra-2.1.so.*
%{_libdir}/libevent_openssl-2.1.so.*
%{_libdir}/libevent_pthreads-2.1.so.*

%files devel
%{_includedir}/*.h
%dir %{_includedir}/event2
%{_includedir}/event2/*.h
%{_libdir}/libevent.so
%{_libdir}/libevent_core.so
%{_libdir}/libevent_extra.so
%{_libdir}/libevent_openssl.so
%{_libdir}/libevent_pthreads.so
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_core.pc
%{_libdir}/pkgconfig/libevent_extra.pc
%{_libdir}/pkgconfig/libevent_openssl.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc
%{_bindir}/event_rpcgen.*


%changelog
* Fri Jun 24 2022 dillon chen <dillon.chen@gmail.com> - 2.1.12-6
- add patch3

* Tue Nov 23 2021 Hu Bin <hubin571@huawei.com> - 2.1.12-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add testcases for event.c apis

* Wed Apr 21 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.1.12-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:use make macros to run check

* Mon Mar 29 2021 panxiaohe <panxiaohe@huawei.com> - 2.1.12-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add debuginfo package and make ELF files stripped
       remove redundant ABI compatibility library

* Thu Mar 18 2021 yang_zhuang_zhuang <yangzhuangzhuang1@huawei.com> - 2.1.12-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Optimize compilation time

* Thu Jul 30 2020 yang_zhuang_zhuang <yangzhuangzhuang1@huawei.com> - 2.1.12-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 2.1.12

* Wed Jul 1 2020 Liquor <lirui130@huawei.com> - 2.1.11-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix undefined-shift in EVUTIL_IS*_ helpers

* Mon Oct 28 2019 chengquan <chengquan3@huawei.com> - 2.1.11-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add global marco of debug_package

* Tue Aug 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.1.11-1
- Package init
