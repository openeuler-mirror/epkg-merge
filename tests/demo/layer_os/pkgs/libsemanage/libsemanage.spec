%define libsepol_version 3.3-1
%define libselinux_version 3.3-1

Name:    libsemanage
Version: 3.3
Release: 3
License: LGPLv2+
Summary: SELinux binary policy manipulation library
URL:     https://github.com/SELinuxProject/selinux/wiki
Source0: https://github.com/SELinuxProject/selinux/releases/download/3.3/libsemanage-%{version}.tar.gz
Source1: semanage.conf

Patch9000: fix-test-failure-with-secilc.patch

BuildRequires: gcc python3-devel bison flex bzip2-devel audit-libs-devel
BuildRequires: libselinux-devel >= %{libselinux_version} swig  libsepol-devel >= %{libsepol_version}
BuildRequires: CUnit-devel gdb-headless

Requires: bzip2-libs audit-libs
Requires: libselinux >= %{libselinux_version}

%description
libsemanage is the policy management library. Using libsepol and
libselinux to interact with the SELinux system, it also calls helper
programs for loading policy and for checking whether the
file_contexts configuration is valid.

%package   devel
Summary:   Header files and libraries used to build policy manipulation tools
Requires:  %{name} = %{version}-%{release}
Provides:  libsemanage-static = %{version}-%{release}
Obsoletes: libsemanage-static < %{version}-%{release}

%description devel
The libsemanage-devel package contains the libraries and header files
needed for developing applications that manipulate SELinux policies.

%package -n python3-libsemanage
Summary:   python3 bindings for libsemanage
Requires:  %{name} = %{version}-%{release} libselinux-python3
Provides:  %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}

%description -n python3-libsemanage
The python3-libsemanage package contains the python bindings for developing
SELinux management applications.

%package_help

%prep
%autosetup -n libsemanage-%{version} -p1

%build
export LDFLAGS="%{?__global_ldflags}"

make clean
%make_build CFLAGS="%{optflags}" swigify
%make_build CFLAGS="%{optflags}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" all
%make_build %{__python3} LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" pywrap

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sharedstatedir}/selinux
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/tmp

make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" install
make PYTHON=%{__python3} DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" install-pywrap

cp %{SOURCE1} %{buildroot}/etc/selinux/semanage.conf
ln -sf  %{_libdir}/libsemanage.so.2 %{buildroot}/%{_libdir}/libsemanage.so

%ldconfig_scriptlets

%check
make test

%files
%license COPYING
%dir %{_sysconfdir}/selinux
%config(noreplace) %{_sysconfdir}/selinux/semanage.conf
%{_libdir}/libsemanage.so.*
%dir %{_libexecdir}/selinux
%dir %{_sharedstatedir}/selinux
%dir %{_sharedstatedir}/selinux/tmp

%files devel
%{_libdir}/libsemanage.a
%{_libdir}/libsemanage.so
%{_libdir}/pkgconfig/libsemanage.pc
%dir %{_includedir}/semanage
%{_includedir}/semanage/*.h

%files -n python3-libsemanage
%{python3_sitearch}/*.so
%{python3_sitearch}/semanage.py*
%{python3_sitearch}/__pycache__/semanage*
%{_libexecdir}/selinux/semanage_migrate_store

%files help
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/ru/man5/*


%changelog
* Fri Mar 18 2022 panxiaohe<panxh.life@foxmail.com> - 3.3-3
- delete useless old version dynamic library

* Tue Mar 15 2022 panxiaohe<panxh.life@foxmail.com> - 3.3-2
- use new version dynamic library

* Tue Dec 14 2021 panxiaohe<panxiaohe@huawei.com> - 3.3-1
- update to 3.3

* Mon Jul 26 2021 yangzhuangzhuang<yangzhuangzhuang1@huawei.com> - 3.1-6
- Remove unnecessary BuildRequires:gdb
 
* Sat Jul 17 2021 luhuaxin <1539327763@qq.com> - 3.1-5
- fix use after free in semanage config parse

* Sat May 22 2021 Hugel<gengqihu1@huawei.com> - 3.1-4
- enabel make test

* Thu Oct 29 2020 Hugel <gengqihu1@huawei.com> - 3.1-3
- remove the dependency on python2

* Mon Aug 17 2020 wangchen <wangchen137@huawei.com> - 3.1-2
- remove ustr

* Sat Jul 25 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.1-1
- update to 3.1

* Thu Mar 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.9-2
- add BuildRequires: gdb

* Thu Sep 5 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9-1
- Package init
