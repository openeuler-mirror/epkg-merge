%define _moduledir %{_libdir}/security
%define _secconfdir %{_sysconfdir}/security

Name: libpwquality
Version: 1.4.4
Release: 5
Summary: Library for password quality checking and generating random passwords.
License: BSD or GPLv2+
URL:     https://github.com/libpwquality/libpwquality/
Source0: https://github.com/libpwquality/libpwquality/releases/download/libpwquality-%{version}/libpwquality-%{version}.tar.bz2

Patch0: modify-pwquality_conf.patch
Patch1: fix-password-similarity.patch
Patch2: fix-doc-about-difok.patch

BuildRequires: gcc cracklib-devel gettext pam-devel
BuildRequires: python3-devel

Recommends: cracklib >= 2.8
Requires: pam

%description
The libpwquality library purpose is to provide common functions for password quality checking and also scoring them based on their apparent randomness. 
The library also provides a function for generating random passwords with good pronounceability.
The library supports reading and parsing of a configuration file.

%package devel
Summary: Support for development of applications using the libpwquality library
Requires: libpwquality = %{version}-%{release}
Requires: pkgconfig

%description devel
Files needed for development of applications using the libpwquality library.
See the pwquality.h header file for the API.

%package -n python3-pwquality
Summary: Python3 bindings for the libpwquality library
Requires: libpwquality = %{version}-%{release}

%description -n python3-pwquality
This package provides Python3 bindings for the libpwquality library.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
#python3
%configure --with-securedir=%{_moduledir} \
	   --with-pythonsitedir=%{python3_sitearch} \
	   --with-python-binary=%{__python3} \
	   --disable-static

%make_build

%install
# python-setuptools >= v60.0.0 changes the SETUPTOOLS_USE_DISTUTILS default value to local,
# it does't use Python's standard library distutils default.
# As a result, failed to build libpwquality.
# Now, set SETUPTOOLS_USE_DISTUTILS value to stdlib
export SETUPTOOLS_USE_DISTUTILS=stdlib
%make_install

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_moduledir}/*.la

mkdir %{buildroot}%{_secconfdir}/pwquality.conf.d

%find_lang libpwquality

%check

%ldconfig_scriptlets

%files -f libpwquality.lang
%license COPYING
%doc README NEWS AUTHORS
%{_bindir}/pwmake
%{_bindir}/pwscore
%{_moduledir}/pam_pwquality.so
%{_libdir}/libpwquality.so.*
%config(noreplace) %{_secconfdir}/pwquality.conf
%{_secconfdir}/pwquality.conf.d

%files devel
%{_includedir}/pwquality.h
%{_libdir}/libpwquality.so
%{_libdir}/pkgconfig/*.pc

%files -n python3-pwquality
%{python3_sitearch}/*.so
%{python3_sitearch}/*.egg-info

%files help
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man3/*
%{_mandir}/man8/*

%changelog
* Tue Aug 23 2022 yixiangzhike <yixiangzhike007@163.com> - 1.4.4-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:change the files order in patch file fix-doc-about-difok.patch

* Wed Aug 10 2022 yixiangzhike <yixiangzhike007@163.com> - 1.4.4-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix doc about difok

* Tue Jul 26 2022 yixiangzhike <yixiangzhike007@163.com> - 1.4.4-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix the libpwquality build failure issue

* Tue Apr 26 2022 zhangruifang2020 <zhangruifang1@h-partners.com> - 1.4.4-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify the changelog

* Sat Jan 23 2021 zoulin <zoulin13@huawei.com> - 1.4.4-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update to 1.4.4

* Thu Oct 29 2020 Hugel <gengqihu1@huawei.com> - 1.4.2-2
- Type:requirement
- ID:NA
- SUG:NA
- DESC:delete python2 package

* Thu Jul 23 2020 Hugel <gengqihu1@huawei.com> - 1.4.2-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update to 1.4.2

* Wed Sep 4 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.4.0-11
- Package init
