%global debug_package %{nil}

Name:     	libevhtp
Version:  	1.2.18
Release:  	5
Summary:  	Libevent based HTTP API.

License:  	BSD-3-Clause
URL:      	https://github.com
Source0:  	https://github.com/criticalstack/libevhtp/archive/1.2.18.tar.gz
Patch9000:  0001-decrease-numbers-of-fd-for-shared-pipe-mode.patch
Patch9001:  0002-evhtp-enable-dynamic-thread-pool.patch
Patch9002:  0003-close-open-ssl.-we-do-NOT-use-it-in-lcrd.patch
Patch9003:  0004-Use-shared-library-instead-static-one.patch
Patch9004:  0005-libevhtp-add-securce-compile-options.patch

BuildRequires: 	git gcc-c++ cmake libevent-devel

%description
Libevent based HTTP API.Libevent's http interface was created as a JIT server, never meant
to be a full-fledged HTTP service. This library attempts to improve on that with the following
features: + design as a fully functional HTTP server + HTTP parser able to process data with a
low memory footprint + use of regular expressions for routing + out-of-the box HTTPS server
This package contains the runtime library.

%package 	devel
Summary: 	Headers for developing programs that will use %{name}
Requires: 	%{name} = %{version}-%{release}

%description 	devel
%{name}-devel contains the header files for developing
applications that want to make use of %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
mkdir -p build
cd build
%cmake -DEVHTP_BUILD_SHARED=ON -DEVHTP_DISABLE_SSL=ON -DLIB_INSTALL_DIR=lib ..
%make_build

%install
rm -rf %{buildroot}
cd build
%make_install

%delete_la_and_a
find %{buildroot} -name '*.cmake' -exec rm -f {} ';'
find %{buildroot} -name '*.so.*' -exec strip {} ';'

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
/usr/lib/%{name}.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/evhtp/*.h
%{_includedir}/evhtp/sys/*.h
/usr/lib/%{name}.so
/usr/lib/pkgconfig/evhtp.pc

%changelog
* Thu Jul 28 2022 fushanqing <fushanqing@kylinos.cn> - 1.2.18-5
- Unified license name specification

* Thu May 05 2022 zhangxiaoyu <zhangxiaoyu58@huawei.com> - 1.2.18-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: update release

* Fri Mar 19 2021 wujing <wujing50@huawei.com> - 1.2.18-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: add secure compile options

* Tue Sep 01 2020 openeuler Buildteam <buildteam@openeuler.org> - 1.2.18-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: modify source0 address

* Wed Apr 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.2.18-1
- Package init

