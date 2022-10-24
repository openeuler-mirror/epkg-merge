Name:		libfastjson
Version:	0.99.9
Release:	2
Summary:	JSON-C - A JSON implementation in C
License:	MIT
URL:		https://github.com/rsyslog/libfastjson
Source0:	http://download.rsyslog.com/%{name}/%{name}-%{version}.tar.gz

BuildRequires: autoconf automake libtool

%description
libfastjson is a fork from json-c, and is currently
under development. The aim of this is not to provide
a slightly modified clone of json-c. It's aim is to
provide: a small library with essential json handling
functions, sufficiently good json support (not 100%
standards compliant), be very fast in processing.

Obsoletes:	%{name} < %{version}-%{release}

%package	devel
Summary:	Development files for libfastjson
Requires:       libfastjson = %{version}-%{release}

%description	devel
provide development files for libfastjson

%prep
%autosetup -p1


%build
autoreconf -iv
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -Wl,-z,relro,-z,now -fstack-protector-strong"
%configure --enable-shared --disable-static

%install
make V=1 DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/lib64/libfastjson.la

%check
make V=1 check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%doc AUTHORS ChangeLog README.html
%{_libdir}/libfastjson.so*

%files devel
%{_includedir}/libfastjson
%{_libdir}/libfastjson.so
%{_libdir}/pkgconfig/libfastjson.pc

%changelog
* Thu Sep 8 2022 panxiaohe <panxh.life@foxmail.com> - 0.99.9-2
- fix obsoletes in spec

* Fri Sep 3 2021 panxiaohe <panxiaohe@huawei.com> - 0.99.9-1
- update to 0.99.9

* Wed Sep 9 2020 wangchen <wangchen137@huawei.com> - 0.99.8-4
- modify the URL of Source0

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.99.8-3
- add requires

* Fri Jan 10 2020 BruceGW <gyl93216@163.com> - 0.99.8-2
- Fix duplicate provides

* Mon Sep 2 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.99.8-1
- Package init
