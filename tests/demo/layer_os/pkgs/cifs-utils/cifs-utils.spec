Name:           cifs-utils
Version:        6.15
Release:        1
Summary:        Utilities for doing and managing mounts of the Linux CIFS filesystem
License:        GPLv3+
URL:            http://linux-cifs.samba.org/cifs-utils/
Source0:        https://download.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}.tar.bz2

BuildRequires:  python3-docutils libcap-ng-devel libtalloc-devel krb5-devel keyutils-libs-devel autoconf
BuildRequires:  automake libwbclient-devel pam-devel pkg-config fdupes gcc
Provides:       pam_cifscreds
Obsoletes:      pam_cifscreds
Requires:       keyutils


%description
The in-kernel CIFS filesystem is generally the preferred method for mounting
SMB/CIFS shares on Linux.

The in-kernel CIFS filesystem relies on a set of user-space tools. That package
of tools is called cifs-utils.Although not really part of Samba proper, these
tools were originally part of the Samba package. For several reasons, shipping
these tools as part of Samba was problematic and it was deemed better to split
them off into their own package.

%package devel
Summary: Files needed for building plugins for cifs-utils

%description devel
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains the header file
necessary for building ID mapping plugins for cifs-utils.

%package help
Summary: Including man files for cifs-utils
Requires: man

%description   help
This contains man files for the using of cifs-utils.

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf -vif
%configure  --prefix=/usr --with-pamdir=%{_libdir}/security  ROOTSBINDIR=%{_sbindir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_libdir}/%{name}/idmapwb.so %{buildroot}%{_sysconfdir}/%{name}/idmap-plugin
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/*
%{_sbindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/idmapwb.so
%{_libdir}/security/pam_cifscreds.so
%dir %{_sysconfdir}/cifs-utils
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.idmap.conf
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.spnego.conf
%ghost  %config(noreplace) %{_sysconfdir}/cifs-utils/idmap-plugin

%files devel
%{_includedir}/cifsidmap.h

%files help
%{_mandir}/man1/*
%{_mandir}/man8/*

%changelog
* Tue Jul 26 2022 zhanchengbin <zhanchengbin1@huawei.com> - 6.15-1
- update cifs-utils version to 6.15-1

* Thu May 5 2022 yanglongkang <yanglongkang@h-partners.com> - 6.14-3
- Fix CVE-2022-27239 and CVE-2022-29869

* Sat Jan 8 2022 yanglongkang <yanglongkang@huawei.com> - 6.14-2
- delete BuildRequires python3-samba

* Tue Nov 16 2021 Wenchao Hao <haowenchao@huawei.com> - 6.14-1
- Update to cifs-utils-6.14

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 6.12-3
- DESC: delete -Sgit from %autosetup, and delete BuildRequires git

* Fri May 7 2021 yanglongkang <yanglongkang@huawei.com> - 6.12-2
- Fix CVE-2021-20208

* Fri Jan 22 2021 yanglongkang <yanglongkang@huawei.com> - 6.12-1
- update to latest v6.12 version

* Wed Jul 15 2020 Zhiqiang Liu <lzhq28@mail.ustc.edu.cn> - 6.10-1
- update to latest v6.10 version

* Tue Jun 30 2020 volcanodragon <linfeilong@huawei.com> - 6.8-6
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESCi:rename patches

* Fri Aug 30 2019 zoujing<zoujing13@huawei.com> - 6.8-5
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESCi:openEuler Debranding

* Tue Aug 20 2019 zoujing<zoujing13@huawei.com> - 6.8-4
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESCi:openEuler Debranding

* Tue Aug 20 2019 zhanghaibo <ted.zhang@huawei.com> - 6.8-3
- correct patch name

* Tue Jul 23 2019 liujiawen <liujiawen10@huawei.com> - 6.8-2.2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:mount.cifs: fix memory leaks

* Wed Jul 10 2019 zhangyujing <zhangyujing1@huawei.com> - 6.8-2.1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:setcifsacl: fix adding ACE when owner sid in unexpected location
       cifs.upcall: fix a compiler warning

* Mon Jul 1 2019 zoujing<zoujing13@huawei.com> - 6.8-2
-  Package Initialization

