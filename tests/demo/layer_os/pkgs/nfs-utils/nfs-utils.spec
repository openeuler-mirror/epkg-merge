%global rpc_uid         29
%global nfsnobody_uid   65534
%global _statdpath /var/lib/nfs/statd

Name:    nfs-utils
Version: 2.5.4
Release: 8
Epoch:   2
Summary: The Linux NFS userland utility package
License: MIT and GPLv2 and GPLv2+ and BSD
URL:     http://sourceforge.net/projects/nfs/

Source0: https://www.kernel.org/pub/linux/utils/nfs-utils/%{version}/%{name}-%{version}.tar.xz

Patch0:  0000-systemd-idmapd-require-rpc-pipefs.patch
Patch1:  0001-correct-the-statd-path-in-man.patch
Patch2:  0002-nfs-utils-set-use-gss-proxy-1-to-enable-gss-proxy-by.patch
Patch3:	 0003-idmapd-Fix-error-status-when-nfs-idmapd-exits.patch
Patch4:	 0004-fix-coredump-in-bl_add_disk.patch
Patch5:  0005-Fix-format-overflow-warning.patch 
Patch6:  0006-nfs-blkmaped-Fix-the-error-status-when-nfs_blkmapd-s.patch
BuildRequires: libevent-devel,libcap-devel, libtirpc-devel libblkid-devel
BuildRequires: krb5-libs >= 1.4 autoconf >= 2.57 openldap-devel >= 2.2
BuildRequires: automake, libtool, gcc, device-mapper-devel
BuildRequires: krb5-devel, libmount-devel
BuildRequires: sqlite-devel, python3-devel
BuildRequires: systemd, pkgconfig, rpcgen


Requires:         rpcbind, sed, gawk, grep, kmod, keyutils, quota
Requires:         libevent libblkid libcap libmount
Requires:         libtirpc >= 0.2.3-1 gssproxy => 0.7.0-3
Recommends:       %{name}-help = %{epoch}:%{version}-%{release}
Requires(pre):    shadow-utils >= 4.0.3-25
Requires(pre):    util-linux
Requires(pre):    coreutils
Requires(pre):    glibc
Requires(preun):  coreutils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(postun): glibc
Requires:         openldap


Provides:  exportfs    = %{epoch}:%{version}-%{release}
Provides:  nfsstat     = %{epoch}:%{version}-%{release}
Provides:  showmount   = %{epoch}:%{version}-%{release}
Provides:  rpcdebug    = %{epoch}:%{version}-%{release}
Provides:  rpc.idmapd  = %{epoch}:%{version}-%{release}
Provides:  rpc.mountd  = %{epoch}:%{version}-%{release}
Provides:  rpc.nfsd    = %{epoch}:%{version}-%{release}
Provides:  rpc.statd   = %{epoch}:%{version}-%{release}
Provides:  rpc.gssd    = %{epoch}:%{version}-%{release}
Provides:  mount.nfs   = %{epoch}:%{version}-%{release}
Provides:  mount.nfs4  = %{epoch}:%{version}-%{release}
Provides:  umount.nfs  = %{epoch}:%{version}-%{release}
Provides:  umount.nfs4 = %{epoch}:%{version}-%{release}
Provides:  sm-notify   = %{epoch}:%{version}-%{release}
Provides:  start-statd = %{epoch}:%{version}-%{release}
Provides:  libnfsidmap = %{epoch}:%{version}-%{release}
Provides:  libnfsidmap%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: libnfsidmap


%description
This is he nfs-utils tools package.
It contains the showmount,mount.nfs,umount.nfs and libnfsidmap

%package   devel
Summary:   Including header files and library for the developing of libnfsidmap library
Requires:  nfs-utils%{?_isa} = %{epoch}:%{version}-%{release}
Requires:  pkgconfig
Provides:  libnfsidmap-devel = %{epoch}:%{version}-%{release}
Provides:  libnfsidmap-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: libnfsidmap-devel

%description devel
This contains dynamic libraries and header files for the developing of
the libnfsidmap library.


%package   help
Summary:   Including man files for nfs-utils
Requires:  man

%description  help
This contains man files for the using of nfs-utils.

%prep
%autosetup -n %{name}-%{version} -p1
find -name \*.py -exec sed -r -i '1s|^#!\s*/usr/bin.*python.*|#!%{__python3}|' {} \;

%build
sh -x autogen.sh
%configure \
    CFLAGS="%{build_cflags} -D_FILE_OFFSET_BITS=64" \
    LDFLAGS="%{build_ldflags}" \
    --enable-mountconfig \
    --enable-ipv6 \
    --with-statdpath=%{_statdpath} \
    --enable-libmount-mount \
    --with-systemd \
    --without-tcp-wrappers \
    --with-pluginpath=%{_libdir}/libnfsidmap

%make_build all

%install
%make_install


install -D -m 644 utils/nfsidmap/id_resolver.conf $RPM_BUILD_ROOT%{_sysconfdir}/request-key.d/id_resolver.conf
install -s -m 755 tools/rpcdebug/rpcdebug $RPM_BUILD_ROOT%{_sbindir}
install -m 644 utils/mount/nfsmount.conf  $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 nfs.conf  $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 support/nfsidmap/idmapd.conf $RPM_BUILD_ROOT%{_sysconfdir}

touch $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/rmtab
mv $RPM_BUILD_ROOT%{_sbindir}/rpc.statd $RPM_BUILD_ROOT/sbin

mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/rpc_pipefs
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/v4recovery
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/exports.d

cd $RPM_BUILD_ROOT%{_unitdir}
ln -s rpc-statd.service nfs-lock.service
ln -s rpc-gssd.service nfs-secure.service
ln -s nfs-server.service nfs.service
ln -s nfs-idmapd.service  nfs-idmap.service

rm -rf $RPM_BUILD_ROOT%{_libdir}/{*.a,*.la}
rm -rf $RPM_BUILD_ROOT%{_libdir}/libnfsidmap/{*.a,*.la}

%check
make check

%pre
if [ -f /var/lock/subsys/rpc.gssd ]; then
    mv /var/lock/subsys/rpc.gssd /var/lock/subsys/rpcgssd
fi

if [ -f /var/lock/subsys/rpc.idmapd ]; then
    mv /var/lock/subsys/rpc.idmapd /var/lock/subsys/rpcidmapd
fi

cat /etc/group | cut -d':' -f 1 | grep rpcuser &> /dev/null
if [ "$?" -ne 0 ]; then
    /usr/sbin/groupadd -g %{rpc_uid} rpcuser &> /dev/null || :
else
    /usr/sbin/groupmod -g %{rpc_uid} rpcuser &> /dev/null || :
fi

cat /etc/passwd | cut -d':' -f 1 | grep rpcuser &> /dev/null
if [ "$?" -ne 0 ]; then
    /usr/sbin/useradd -l -c "RPC Service User" -r -g %{rpc_uid} \
        -s /sbin/nologin -u %{rpc_uid} -d /var/lib/nfs rpcuser &> /dev/null || :
else
 /usr/sbin/usermod -u %{rpc_uid} -g %{rpc_uid} rpcuser &> /dev/null || :
fi



cat /etc/group | cut -d':' -f 3 | grep %{nfsnobody_uid} &> /dev/null
if [ "$?" -ne 0 ]; then
    /usr/sbin/groupadd -g %{nfsnobody_uid} nfsnobody &> /dev/null || :
fi

cat /etc/passwd | cut -d':' -f 3 | grep %{nfsnobody_uid} &> /dev/null
if [ $? -ne 0 ]; then
    /usr/sbin/useradd -l -c "Anonymous NFS User" -r -g %{nfsnobody_uid} \
    -s /sbin/nologin -u %{nfsnobody_uid} -d /var/lib/nfs nfsnobody &> /dev/null || :
fi

%post
if [ $1 -eq 1 ] ; then
    /bin/systemctl enable nfs-client.target &> /dev/null  || :
    /bin/systemctl start nfs-client.target  &> /dev/null  || :
fi

%systemd_post nfs-server
/bin/systemctl try-restart gssproxy  &> /dev/null || :

%preun
if [ $1 -eq 0 ]; then
    %systemd_preun nfs-client.target
    %systemd_preun nfs-server.service
    /bin/systemctl stop var-lib-nfs-rpc_pipefs.mount &> /dev/null || :
fi

%postun
%systemd_postun_with_restart  nfs-client.target
%systemd_postun_with_restart  nfs-server

/bin/systemctl --system daemon-reload &> /dev/null  || :


%files
%doc support/nfsidmap/AUTHORS linux-nfs/README linux-nfs/THANKS
%license support/nfsidmap/COPYING
%config(noreplace) /etc/nfsmount.conf
%config(noreplace) %{_sharedstatedir}/nfs/etab
%config(noreplace) %{_sharedstatedir}/nfs/rmtab
%config(noreplace) %{_sysconfdir}/idmapd.conf
%config(noreplace) %{_sysconfdir}/request-key.d/id_resolver.conf
%config(noreplace) %{_sysconfdir}/nfs.conf
%dir %{_sysconfdir}/exports.d
%dir %{_sharedstatedir}/nfs
%dir %{_sharedstatedir}/nfs/v4recovery
%dir %{_sharedstatedir}/nfs/rpc_pipefs
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd/sm
%dir %attr(700,rpcuser,rpcuser) %{_sharedstatedir}/nfs/statd/sm.bak
%ghost %attr(644,rpcuser,rpcuser) %{_statdpath}/state
%attr(4755,root,root) /sbin/mount.nfs
/sbin/{rpc.statd,nfsdcltrack,osd_login,mount.nfs4,umount.*,nfsdcld}
%{_sbindir}/*
%{_prefix}/lib/systemd/*/*
%{_libdir}/libnfsidmap.so.*
%{_libdir}/libnfsidmap/*.so

%files devel
%{_includedir}/nfsidmap.h
%{_includedir}/nfsidmap_plugin.h
%{_libdir}/pkgconfig/libnfsidmap.pc
%{_libdir}/libnfsidmap.so

%files help
%{_mandir}/*/*

%changelog
* Tue Sep 6 2022 zhanchengbin <zhanchengbin1@huawei.com> - 2:2.5.4-8
- nfs-blkmapd: Fix the error status when nfs-blkmapd stops

* Thu Aug 11 2022 xueyamao <xueyamao@ktlinos.cn> - 2:2.5.4-7
- systemd: Fix format-overflow warning.

* Sat Apr 16 2022 Wu Bo <wubo40@huawei.com> - 2.5.4-6
- Update epoch version to 2. In order to fix the upgrade issues.

* Fri Apr 8 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 2.5.4-5
- set use-gss-proxy to true in nfs.conf to be consistent with the
  description of 0002-nfs-utils-set-use-gss-proxy-1-to-enable-gss-proxy-by.patch

* Mon Mar 7 2022 yanglongkang <yanglongkang@h-partners.com> - 2.5.4-4
- fix nfs-blkmapd service core dump

* Thu Feb 24 2022 Wu Bo <wubo40@huawei.com> - 2.5.4-3
- idmapd Fix error status when nfs idmapd exits

* Sat Jan 29 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 2.5.4-2
- In order to be consistent with the old versions, here we set
  use-gss-proxy to true in nfs.conf.

* Thu Nov 18 2021 Wenchao Hao <haowenchao@huawei.com> - 2.5.4-1
- update nfs-utils version to 2.5.4-1

* Thu Dec 17 2020 yanglongkang <yanglongkang@huawei.com> - 2.5.1-2
- set help package as install requires

* Thu Jul 16 2020 wuguanghao <wuguanghao3@huawei.com> - 2.5.1-1
- update nfs-utils version to 2.5.1-1

* Tue Jun 30 2020 volcanodragon <linfeilong@huawei.com> - 2.4.2-4
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:rename patch

* Sat Mar 28 2020 hy <eulerstoragemt@huawei.com> - 2.4.2-3
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:add make check

* Fri Jan 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.2-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:stop the var-lib-nfs-rpc_pipefs.mount before remove the package

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.2-1
- Type:enhancemnet
- ID:NA
- SUG:NA
- DESC:update the package from 2.3.3 version to 2.4.2

* Sun Dec 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.3.3-5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:Modify the wrong service file name in spec file

* Sun Sep 29 2019 zhanghaibo <ted.zhang@huawei.com> - 2.3.3-4
- Remove some comments

* Thu Sep 05 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.3.3-3
- Package init
