Name:           libtirpc
Version:        1.3.2
Release:        2
Summary:        Transport-independent RPC library
License:        SISSL and BSD
URL:            http://git.linux-nfs.org/?p=steved/libtirpc.git;a=summary
Source0:        http://downloads.sourceforge.net/libtirpc/%{name}-%{version}.tar.bz2
Patch0:	        0001-update-libtirpc-to-enable-tcp-port-listening.patch
Patch1:         CVE-2021-46828.patch
BuildRequires:  automake autoconf libtool pkgconfig krb5-devel

%description
Libtirpc is a Transport-Independent RPC library for Linux

%package        devel
Summary:        Development files for the %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig man-db

%description    devel
The %{name}-devel package contains development files for %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
sh autogen.sh
autoreconf -fisv
%configure
%make_build

%install
%make_install libdir=/%{_lib} pkgconfigdir=%{_libdir}/pkgconfig
%delete_la

mv %{buildroot}%{_mandir}/man3 %{buildroot}%{_mandir}/man3t

%ldconfig_scriptlets

%post devel
%postun devel

%files
%defattr(-,root,root)
%doc AUTHORS
%license COPYING
/%{_lib}/*.so.*
%config(noreplace)%{_sysconfdir}/netconfig
%config(noreplace)%{_sysconfdir}/bindresvport.blacklist

%files          devel
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
/%{_lib}/*.a
/%{_lib}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/tirpc/*

%files          help
%defattr(-,root,root)
%doc ChangeLog NEWS README
%{_mandir}/*/*

%changelog
* Thu Jul 21 2022 xuchenchen <xuchenchen@kylinos.cn> - 1.3.2-2
- Type: fix CVE
- ID:CVE-2021-46828
- SUG:NA
- DESC: fix CVE-2021-46828

* Sat Mar 19 2022 xihaochen <xihaochen@h-partners.com> - 1.3.2-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC: update libtirpc to 1.3.2

* Wed Jan 27 2021 xihaochen <xihaochen@huawei.com> - 1.3.1-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC: update libtirpc to 1.3.1

* Tue Jul 28 2020 lunankun <lunankun@huawei.com> -1.2.6-1
- Type:update
- Id:NA
- SUG:NA
- DESC:update to libtirpc-1.2.6

* Thu Aug 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.1.4-1
- Package init
