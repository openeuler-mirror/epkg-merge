Name:		iproute
Version:	5.15.0
Release:	5
Summary:	Linux network configuration utilities
License:	GPLv2+ and Public Domain
URL:		https://kernel.org/pub/linux/utils/net/iproute2/
Source0:	https://mirrors.edge.kernel.org/pub/linux/utils/net/iproute2/iproute2-%{version}.tar.xz

Patch1:         bugfix-iproute2-3.10.0-fix-maddr-show.patch         
Patch2:         bugfix-iproute2-change-proc-to-ipnetnsproc-which-is-private.patch

Patch6000:      backport-devlink-fix-devlink-health-dump-command-without-arg.patch
Patch6001:      backport-ip-Fix-size_columns-for-very-large-values.patch
Patch6002:      backport-ip-Fix-size_columns-invocation-that-passes-a-32-bit-.patch
Patch6003:      backport-l2tp-fix-typo-in-AF_INET6-checksum-JSON-print.patch
Patch6004:      backport-libnetlink-fix-socket-leak-in-rtnl_open_byproto.patch
Patch6005:      backport-lnstat-fix-buffer-overflow-in-header-output.patch
Patch6006:      backport-lnstat-fix-strdup-leak-in-w-argument-parsing.patch
Patch6007:      backport-q_cake-allow-changing-to-diffserv3.patch
Patch6008:      backport-tc-em_u32-fix-offset-parsing.patch
Patch6009:      backport-tc-flower-Fix-buffer-overflow-on-large-labels.patch
Patch6010:      backport-tc_util-Fix-parsing-action-control-with-space-and-sl.patch
Patch6011:      backport-tipc-fix-keylen-check.patch

Patch6012:      backport-bridge-Fix-memory-leak-when-doing-fdb-get.patch
Patch6013:      backport-ip-address-Fix-memory-leak-when-specifying-device.patch
Patch6014:      backport-ip-neigh-Fix-memory-leak-when-doing-get.patch
Patch6015:      backport-mptcp-Fix-memory-leak-when-doing-endpoint-show.patch
Patch6016:      backport-mptcp-Fix-memory-leak-when-getting-limits.patch

BuildRequires:	gcc bison elfutils-libelf-devel flex iptables-devel
BuildRequires:  libmnl-devel libselinux-devel pkgconfig libbpf-devel
Requires:       libbpf psmisc

Provides:       /sbin/ip iproute-tc tc 
Obsoletes:      iproute-tc 

%description
Iproute2 is a collection of user-space utilities to set up networking
under Linux from the command-line. It can inspect and configure,
among other things: interface paramters, IP addresses, routing,
tunnels, bridges, packet transformations (IPsec, etc.), and Quality
of Service.

%package        devel
Summary:        Header files for iprout2
License:        GPLv2+
Provides:       iproute-static = %{version}-%{release}
Obsoletes:      iproute-static < %{version}-%{release}

%description    devel
Header files for iprout2

%package_help

%prep
%autosetup -n %{name}2-%{version} -p1

%build
export LIBDIR='%{_libdir}'
export IPT_LIB_DIR='/%{_lib}/xtables'
%configure
%make_build

%install
export CONFDIR='%{_sysconfdir}/iproute2'
export SBINDIR='%{_sbindir}'
export LIBDIR='%{_libdir}'
export DOCDIR='%{_docdir}'

%make_install 

install -m 0755 -d %{buildroot}%{_includedir}
install -m 0644 include/libnetlink.h %{buildroot}%{_includedir}/libnetlink.h
install -m 0644 lib/libnetlink.a %{buildroot}%{_libdir}/libnetlink.a

%files
%defattr(-,root,root)
%license COPYING
%doc README
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/iproute2/*
%{_sbindir}/*
%{_libdir}/tc/*
%{_datadir}/bash-completion/completions/*

%files         devel
%defattr(-,root,root)
%license COPYING
%{_libdir}/libnetlink.a
%{_includedir}/*

%files         help
%defattr(-,root,root)
%doc README
%{_mandir}/*

%changelog
* Mon Oct 10 2022 jiangheng<jiangheng14@huawei.com> - 5.15.0-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:bridge: fix memory leak when doing fdb get
       mptcp: fix memory leak when doing 'endpoint show'
       mptcp: fix memory leak when getting limits
       ip neigh: fix memory leak when doing 'get'
       ip address: fix memory leak when specifying device
       fix marco expansion in changelog

* Fri Aug 26 2022 sunsuwan<sunsuwan3@huawei.com> - 5.15.0-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:lnstat: fix buffer overflow in header output 
       libnetlink: fix socket leak in rtnl_open_byptoyo
       lnstat: fix strdup leak in w argument parsing
       q_cake: allow fix buffer overflow on large labels
       tc flower: fix buffer overflow on large labels
       tc_tuil: fix parsing action control with space and sl
       tipc: fix keylen check
       fix devlink health dump command without arg
       tc: em_u32: fix offset parsing
       l2tp fix typo in AF_INET6 checksum JSON print
       ip: Fix size_columns() for very large values
       ip: Fix size_columns() invocation that passes a 32-bit quantity

* Tue Mar 01 2022 jiangheng<jiangheng12@huawei.com> - 5.15.0-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: remove libcap-devel dependency

* Mon Feb 21 2022 jiangheng<jiangheng12@huawei.com> - 5.15.0-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: remove libdb-devel dependency

* Fri Nov 26 2021 jiangheng <jiangheng12@huawei.com> - 5.15.0-1
- DESC: update to 5.15.0

* Mon Aug 02 2021 chenyanpanHW <chenyanpan@huawei.com> - 5.10.0-2
- DESC: delete -S git from autosetup, and delete BuildRequires git

* Tue Jan 26 2021 xihaochen<xihaochen@huawei.com> - 5.10.0-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC: update iproute to 5.10.0

* Thu Dec 10 2020 zhouyihang <zhouyihang3@huawei.com> - 5.7.0-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:modify fix of get_tc_lib err

* Thu Sep 24 2020 zhouyihang <zhouyihang3@huawei.com> - 5.7.0-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix get_tc_lib err

* Wed Jul 22 2020 hanzhijun <hanzhijun1@huawei.com> - 5.7.0-1
- update to 5.7.0

* Mon Jan 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.4.0-2
- fix maddr show and change proc to ipnetnsproc

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.4.0-1
- update to 5.4.0

* Fri Oct 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.2.0-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add the bugfix about iproute

* Thu Sep 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.2.0-1
- Package init
