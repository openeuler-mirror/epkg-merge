Name: libestr
Version: 0.1.11
Release: 1
Summary: String handling essentials library

License: LGPLv2+
URL: http://libestr.adiscon.com/
Source0: http://libestr.adiscon.com/files/download/libestr-%{version}.tar.gz

BuildRequires: gcc

%description
libestr is a library for some string essentials. This package compiles the string handling essentials library
used by the Rsyslog daemon.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --disable-static --with-pic

%make_build

%install
%make_install
rm -f %{buildroot}/%{_libdir}/*.{a,la}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%license COPYING
%doc README AUTHORS ChangeLog
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/libestr.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libestr.pc

%changelog
* Mon May 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.1.11-1
- Upgrade version to 0.1.11

* Thu Aug 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.1.9-12
- Package init
