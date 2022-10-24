%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Libcap-ng is a library used for posix capabilities programming
Name: libcap-ng
Version: 0.8.2
Release: 1
License: LGPLv2+ and GPLv2+
URL: http://people.redhat.com/sgrubb/libcap-ng
Source0: https://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
BuildRequires: gcc, kernel-headers >= 2.6.11, libattr-devel
Provides: %{name}-utils = %{version}-%{release}
Obsoletes: %{name}-utils < %{version}-%{release}

%description
The libcap-ng library is intended to make programming with posix
capabilities much easier than the traditional libcap library.It
includes utilities that can analyse all currently running applications
and print out any capabilities and whether or not it has an open
ended bounding set.

%package devel
Summary: Development libraries and header files for %{name}
License: LGPLv2+
Requires: kernel-headers >= 2.6.11
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains the files needed for developing
applications that need to use the %{name} library.

%package python3
Summary: Python3 bindings for libcap-ng library
License: LGPLv2+
BuildRequires: python3-devel swig
Requires: %{name} = %{version}-%{release}

%description python3
The %{name}-python3 package contains the bindings so that %{name} and
can be used by python3 applications.

%package_help

%prep
%autosetup -p1

%build
%configure --libdir=/%{_lib} --with-python=no --with-python3
make CFLAGS="%{optflags}" %{?_smp_mflags}

%install
%make_install

# Move from %{_lib} to %{_libdir}
rm -f $RPM_BUILD_ROOT/%{_lib}/%{name}.so
rm -f $RPM_BUILD_ROOT/%{_lib}/libdrop_ambient.so
mkdir -p $RPM_BUILD_ROOT%{_libdir}
VLIBNAME=$(ls $RPM_BUILD_ROOT/%{_lib}/%{name}.so.*.*.*)
LIBNAME=$(basename $VLIBNAME)
ln -s ../../%{_lib}/$LIBNAME $RPM_BUILD_ROOT%{_libdir}/%{name}.so
ln -s ../../%{_lib}/libdrop_ambient.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/libdrop_ambient.so
mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libcap-ng.a $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libdrop_ambient.a $RPM_BUILD_ROOT%{_libdir}

%delete_la

%check
make check

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license COPYING.LIB COPYING
%attr(0755,root,root) %{_bindir}/*
/%{_lib}/libcap-ng.so.*
/%{_lib}/libdrop_ambient.so.*

%files devel
%attr(0644,root,root) %{_includedir}/cap-ng.h
%{_libdir}/libcap-ng.so
%{_libdir}/libcap-ng.a
%{_libdir}/libdrop_ambient.so
%{_libdir}/libdrop_ambient.a
%attr(0644,root,root) %{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc

%files python3
%attr(755,root,root) %{python3_sitearch}/*
%{python3_sitearch}/capng.py*

%files help
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_mandir}/man7/*
%attr(0644,root,root) %{_mandir}/man8/*

%changelog
* Fri Dec 24 2021 yixiangzhike <yixiangzhike007@163.com> - 0.8.2-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update to 0.8.2

* Fri Sep 24 2021 fuanan <fuanan3@huawei.com> - 0.8.1-1
- update version to 0.8.1

* Thu Jan 21 2021 wangchen<wangchen137@huawei.com> - 0.7.11-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update to 0.7.11

* Thu Oct 29 2020 wangchen<wangchen137@huawei.com> - 0.7.10-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:remove python2

* Wed Sep 9 2020 wangchen<wangchen137@huawei.com> - 0.7.10-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify the URL of Source0

* Thu Apr 16 2020 zhangchenfeng<zhangchenfeng1@huawei.com> - 0.7.10-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: upgrade version to 0.7.10

* Sat Mar 21 2020 liufeng<liufeng111@huawei.com> - 0.7.9-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add patch

* Tue Jan 7 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.7.9-7
- Delete unused patch

* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.7.9-6
- Delete unused patch

* Mon Sep 09 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.7.9-5
- Package init
