Name:           libwebsockets
Version:        4.3.0
Release:        4
Summary:        A lightweight C library for Websockets
License:        LGPLv2 and Public Domain and BSD and MIT and zlib
URL:            https://libwebsockets.org
Source0:        https://github.com/warmcat/libwebsockets/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch9001:	0001-add-secure-compile-option-in-Makefile.patch
Patch9002:	0002-solve-the-BEP-problem.patch
Patch9003:	0003-route-extend-lws_route_uidx_t-from-1-byte-to-2-bytes.patch

BuildRequires:  cmake openssl-devel zlib-devel libev-devel gcc gcc-c++

Provides:       bundled(sha1-hollerbach) bundled(base64-decode) bundled(ssl-http2)

%description
Libwebsockets (LWS) is a flexible, lightweight pure C library for implementing modern
network protocols easily with a tiny footprint, using a nonblocking event loop.

%package        devel
Summary:        Headers for developing programs that will use %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

Provides:       %{name}-tests
Obsoletes:      %{name}-tests

%description    devel
This package contains the header files needed for developing
%{name} applications.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1
%build
mkdir -p build
cd build
%cmake \
    -D LWS_WITH_HTTP2=ON \
    -D LWS_IPV6=ON \
    -D LWS_WITH_ZIP_FOPS=ON \
    -D LWS_WITH_SOCKS5=ON \
    -D LWS_WITH_RANGES=ON \
    -D LWS_WITH_ACME=ON \
    -D LWS_WITH_LIBUV=OFF \
    -D LWS_WITH_LIBEV=OFF \
    -D LWS_WITH_LIBEVENT=OFF \
    -D LWS_WITH_FTS=ON \
    -D LWS_WITH_THREADPOOL=ON \
    -D LWS_UNIX_SOCK=ON \
    -D LWS_WITH_HTTP_PROXY=ON \
    -D LWS_WITH_DISKCACHE=ON \
    -D LWS_WITH_LWSAC=ON \
    -D LWS_LINK_TESTAPPS_DYNAMIC=ON \
    -D LWS_WITHOUT_BUILTIN_GETIFADDRS=ON \
    -D LWS_USE_BUNDLED_ZLIB=OFF \
    -D LWS_WITHOUT_BUILTIN_SHA1=ON \
    -D LWS_WITH_STATIC=OFF \
    -D LWS_WITHOUT_CLIENT=OFF \
    -D LWS_WITHOUT_SERVER=OFF \
    -D LWS_WITHOUT_TESTAPPS=OFF \
    -D LWS_WITHOUT_TEST_SERVER=ON \
    -D LWS_WITHOUT_TEST_SERVER_EXTPOLL=ON \
    -D LWS_WITHOUT_TEST_PING=ON \
    -D LWS_WITHOUT_TEST_CLIENT=ON \
    -D LWS_WITHOUT_EXTENSIONS=OFF \
    ..

%make_build

%install
cd build
%make_install

%delete_la_and_a
find %{buildroot} -name '*.cmake' -exec rm -f {} ';'
find %{buildroot} -name '*_static.pc' -exec rm -f {} ';'

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_bindir}/%{name}-test-*
%{_datadir}/%{name}-test-server/


%files help
%defattr(-,root,root)
%doc changelog README.md READMEs/

%changelog
* Thu May 05 2022 zhangxiaoyu <zhangxiaoyu58@huawei.com> - 4.3.0-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:extend lws_route_uidx_t from 1 byte to 2 bytes

* Tue May 03 2022 zhangxiaoyu <zhangxiaoyu58@huawei.com> - 4.3.0-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix changelog error

* Tue Nov 30 2021 zhangxiaoyu <zhangxiaoyu58@huawei.com> - 4.3.0-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:set LWS_WITHOUT_EXTENSIONS option OFF

* Mon Nov 29 2021 zhangxiaoyu <zhangxiaoyu58@huawei.com> - 4.3.0-1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add build require gcc and gcc-c++

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 4.0.20-8
- DESC:delete -S git from autosetup, and delete BuildRequires git

* Mon Jun 28 2021 lifeng <lifeng68@huawei.com> - 4.0.20-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add build require gcc and gcc-c++

* Mon May 10 2021 wujing <wujing50@huawei.com> - 4.0.20-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:solve the BEP problem

* Tue Mar 16 2021 lifeng <lifeng68@huawei.com> - 4.0.20-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add secure compile options

* Fri Feb 19 2021 lifeng <lifeng68@huawei.com> - 4.0.20-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove unused head file directory

* Fri Nov 20 2020 jikui <jikui2@huawei.com> - 4.0.20-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify spec file

* Tue Aug 4 2020 zhangxiaoyu <zhangxiaoyu58@huawei.com> - 4.0.20-2
- Type:requirement
- ID:NA
- SUG:NA
- DESC:modify spec file

* Wed Jul 29 2020 zhangxiaoyu <zhangxiaoyu58@huawei.com> - 4.0.20-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update to 4.0.20

* Tue Jun 9 2020 zhujunhao <zhujunhao8@huawei.com> - 4.0.1-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update to 4.0.1

* Tue Jan 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.2-3
- Type:bugfix
- ID:NA
- SUG:reboot
- DESC:add bind now secure compile option

* Mon Sep 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.4.2-2
- Package init
