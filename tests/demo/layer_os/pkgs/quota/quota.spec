Name:      quota
Version:   4.06
Epoch:     1
Release:   4
Summary:   Linux Diskquota system as part of the Linux kernel
License:   BSD and GPLv2 and GPLv2+ and LGPLv2+
URL:       http://sourceforge.net/projects/linuxquota/

Source0:   http://downloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.gz
Source1:   quota_nld.service
Source2:   quota_nld.sysconfig
Source3:   rpc-rquotad.service
Source4:   rpc-rquotad.sysconfig

Patch0: 0000-Limit-number-of-comparison-characters-to-4.patch
Patch1: 0001-Limit-maximum-of-RPC-port.patch
Patch2: 0002-quotaio_xfs-Warn-when-large-kernel-timestamps-cannot.patch

BuildRequires:     autoconf, automake, coreutils, rpcgen, systemd, gcc
BuildRequires:     e2fsprogs-devel, gettext-devel, openldap-devel
BuildRequires:     pkgconfig(dbus-1), pkgconfig(libnl-3.0) >= 3.1, pkgconfig(libnl-genl-3.0), pkgconfig(libtirpc)
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
Requires:          rpcbind

Provides:          %{name}-doc = %{epoch}:%{version}-%{release}
Obsoletes:         %{name}-doc
Provides:          %{name}-nld = %{epoch}:%{version}-%{release}
Obsoletes:         %{name}-nld
Provides:          %{name}-nls = %{epoch}:%{version}-%{release}
Obsoletes:         %{name}-nls
Provides:          %{name}-rpc = %{epoch}:%{version}-%{release}
Obsoletes:         %{name}-rpc
Provides:          %{name}-warnquota = %{epoch}:%{version}-%{release}
Obsoletes:         %{name}-warnquota


%description
Tools and patches for the Linux Diskquota system as part of the Linux kernel
It also include quota_nld daemon,


%package        devel
Summary:        Including header files for the developing of quota RPC
License:        GPLv2
Requires:       quota  = %{epoch}:%{version}-%{release}


%description    devel
This contains  header files for the developing of quota RPC.


%package        help
Summary:        Including man files for quota
Requires:       man

%description    help
This contains man files for the using of quota.


%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf -fi
%configure \
    --enable-bsd-behaviour \
    --enable-ext2direct=yes \
    --enable-ldapmail=yes \
    --disable-libwrap \
    --enable-netlink=yes \
    --enable-nls \
    --disable-rpath \
    --enable-rpc=yes \
    --enable-rpcsetquota=yes \
    --disable-silent-rules \
    --disable-xfs-roothack
make


%install
%make_install

install -D -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/quota_nld.service
install -D -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/quota_nld
install -D -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/rpc-rquotad.service
install -D -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rpc-rquotad

%find_lang %{name}

%check
make check


%post
%systemd_post quota_nld.service rpc-rquotad.service

%preun
%systemd_preun quota_nld.service rpc-rquotad.service

%postun
%systemd_postun_with_restart quota_nld.service rpc-rquotad.service



%files -f %{name}.lang
%license COPYING
%doc Changelog
%{_bindir}/*
%{_sbindir}/*
%{_unitdir}/*.service
%config(noreplace) %{_sysconfdir}/*
%exclude %{_docdir}/%{name}

%files devel
%doc doc/* ldap-scripts
%dir %{_includedir}/rpcsvc
%{_includedir}/rpcsvc/*


%files help
%{_mandir}/man*/*

%changelog
* Tue Oct 11 2022 huangduirong <huangduirong@huawei.com> - 1:4.06-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Move autoreconf to build

* Tue Jun 29 2021 zhouwenpei <zhouwenpei1@huawei.com> - 1:4.06-3
- add buildrequire gcc.

* Wed Mar 31 2021 xieliuhua <xieliuhua@huawei.com> - 1:4.06-2
- fix Warn when large kernel timestamps cannot be handled

* Thu Jan 14 2021 yanglongkang <yanglongkang@huawei.com> - 1:4.06-1
- Upgrade to 4.06

* Tue Jun 30 2020 volcanodragon <linfeilong@huawei.com> - 1:4.05-2
- rename patches

* Sat Jan 11 2020 renxudong <renxudong1@huawei.com> - 1:4.05-1
- Upgrade to 4.05

* Sun Sep 29 2019 zhanghaibo <ted.zhang@huawei.com> - 1:4.04-11
- Remove some comments

* Fri Sep 6 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:4.04-10
- Package init
