Name:		ethtool
Epoch:		2
Version:	5.19
Release:	1
Summary:	Settings tool for Ethernet NICs
License:	GPLv2
URL:		https://www.kernel.org/pub/software/network/ethtool
Source0:	https://www.kernel.org/pub/software/network/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	gcc
BuildRequires:	libmnl-devel
Conflicts:      filesystem < 3

%description
Ethtool is the standard Linux utility for controlling network drivers and 
hardware, particularly for wired Ethernet devices. It can be used to:

  - Get identification and diagnostic information
  - Get extended device statistics
  - Control speed, duplex, autonegotiation and flow control for Ethernet devices
  - Control checksum offload and other hardware offload features
  - Control DMA ring sizes and interrupt moderation
  - Control receive queue selection for multiqueue devices
  - Upgrade firmware in flash memory

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure
%make_build

%install
%make_install

%check
make check

%files
%defattr(-,root,root)
%doc AUTHORS 
%license COPYING LICENSE
%{_sbindir}/%{name}
%dir %{_datadir}/bash-completion/
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/ethtool

%files          help
%defattr(-,root,root)
%doc ChangeLog* NEWS README
%{_mandir}/man8/%{name}.8*

%changelog
* Mon Oct 3 2022 tianlijing <tianlijing@kylinos.cn> - 2:5.19-1
- update to 5.19

* Tue Sep 20 2022 xiaojiantao <xiaojiantao1@h-partners.com> - 2:5.15-3
- Type:requirement
- Id:NA
- SUG:NA
- DESC:add support to set or get rx buf len and tx push by ethtool

* Fri Sep 02 2022 gaihuiying <eaglgai@163.com> - 2:5.15-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix memory free operation after send_ioctl call fails

* Sat Mar 19 2022 xihaochen <xihaochen@h-partners.com> - 2:5.15-1
- Type:requirement
- Id:NA
- SUG:NA
- DESC:update ethtool version to 5.15

* Wed Jul 07 2021 xuguangmin <xuguangmin@kylinos.cn> - 2:5.12-1
- Type:requirement
- Id:NA
- SUG:NA
- DESC:update ethtool version to 5.12

* Fri Sep 25 2020 zhouyihang <zhouyihang3@huawei.com> - 2:5.7-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:netlink fix error message suppression

* Wed Jul 29 2020 liulong <liulong20@huawei.com> - 2:5.7-1
- Type:requirement
- Id:NA
- SUG:NA
- DESC:update ethtool version to 5.7

* Wed Mar 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 2:5.3-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:enable developer use cases

* Thu Oct 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 2:5.3-1
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:update to 5.3

* Wed Sep 4 2019 openEuler Buildteam <buildteam@openeuler.org> - 2:4.17-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add requires

* Thu Aug 22 2019 openEuler Buildteam <buildteam@openeuler.org> - 2:4.17-3
- Package Init

