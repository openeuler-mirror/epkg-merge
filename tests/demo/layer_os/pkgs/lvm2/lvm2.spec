%global use_cluster 1
%global use_cmirror 1
%global use_lockd_sanlock 1
%global use_lockd_dlm 1
%ifnarch i686
  %global use_cluster 0
  %global use_cmirror 0
  %global use_lockd_dlm 0
%endif

%ifnarch x86_64 aarch64
  %global use_lockd_sanlock 0
%endif

%if %{use_cluster}
  %global configure_cluster --with-cluster=internal --with-clvmd=corosync
  %if %{use_cmirror}
    %global configure_cmirror --enable-cmirrord
  %endif
%else
  %global configure_cluster --with-cluster=internal --with-clvmd=none
%endif

%if %{use_lockd_dlm}
%global configure_lockd_dlm --enable-lvmlockd-dlm
%endif

%if %{use_lockd_sanlock}
%global configure_lockd_sanlock --enable-lvmlockd-sanlock
%endif

%global libselinux_version 1.30.19-4
%global persistent_data_version 0.7.0-0.1.rc6
%global sanlock_version 3.3.0-2
%global device_mapper_version 1.02.182
%global systemd_version 189-3
%global dracut_version 002-18
%global util_linux_version 2.24
%global bash_version 4.0
%global corosync_version 1.99.9-1
%global resource_agents_version 3.9.5-12
%global dlm_version 4.0.6-2

Name:      lvm2
Version:   2.03.16
Release:   1
Epoch:     8
Summary:   Tools for logical volume management
License:   GPLv2+ and LGPLv2.1 and BSD
URL:       http://sourceware.org/lvm2
Source0:   https://sourceware.org/pub/lvm2/releases/LVM2.2.03.16.tgz
Patch1:    0001-lvm2-set-default-preferred_names.patch
Patch2:    0002-lvm2-default-allow-changes-with-duplicate-pvs.patch
Patch3:    0003-bugfix-lvm2-add-SSD.patch
Patch4:    0004-bugfix-add-timeout-when-fail-to-wait-udev.patch
Patch5:    0005-bugfix-fix-the-code-maybe-lead-to-buffer-over-bound-access.patch
Patch6:    0006-enhancement-modify-default-log-level-to-error-level.patch
Patch7:    0007-enhancement-add-dfx-log.patch
Patch8:    0008-enhancement-syslog-more-when-use-libdevmapper-so.patch
Patch9:    0009-enhancement-log-it-when-disk-slow.patch
Patch10:   0010-bugfix-lvm2-fix-the-reuse-of-va_list.patch
Patch11:   0011-13-dm-disk.rules-check-DM_NAME-before-create-symlink.patch
Patch12:   0012-lvm-code-reduce-cyclomatic-complexity.patch
Patch13:   0013-_vg_read_raw_area-fix-segfault-caused-by-using-null-.patch

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libselinux-devel >= %{libselinux_version}, libsepol-devel
BuildRequires: libblkid-devel >= %{util_linux_version}
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: libaio-devel
BuildRequires: module-init-tools
BuildRequires: pkgconfig
BuildRequires: systemd-devel
BuildRequires: systemd-units
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-dbus
BuildRequires: python3-pyudev
BuildRequires: device-mapper-persistent-data >= %{persistent_data_version}
BuildRequires: device-mapper-event

%if %{use_cluster}
BuildRequires: corosynclib-devel >= %{corosync_version}
%endif
%if %{use_cluster} || %{use_lockd_dlm}
BuildRequires: dlm-devel >= %{dlm_version}
%endif
%if %{use_lockd_sanlock}
BuildRequires: sanlock-devel >= %{sanlock_version}
%endif

Requires: bash >= %{bash_version}
Requires: module-init-tools
Requires: device-mapper-persistent-data >= %{persistent_data_version}
Requires: device-mapper-event = %{?epoch}:%{device_mapper_version}-%{release}
Recommends: %{name}-help = %{epoch}:%{version}-%{release}
Requires(post):   systemd-units >= %{systemd_version}, systemd-sysv
Requires(preun):  systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

Provides:  %{name}-libs
Obsoletes: %{name}-libs

%description
lvm2 refers to the userspace toolset that provide logical volume management facilities on linux.

%package devel
Summary:   lvm2 devel files
License:   LGPLv2
Requires:  %{name} = %{?epoch}:%{version}-%{release}
Requires:  pkgconfig
Requires:  device-mapper = %{?epoch}:%{device_mapper_version}-%{release}
Provides:  device-mapper-devel = %{?epoch}:%{device_mapper_version}-%{release}
Obsoletes: device-mapper-devel
Provides:  device-mapper-event-devel = %{?epoch}:%{device_mapper_version}-%{release}
Obsoletes: device-mapper-event-devel

%description devel
This package contains all include files, libraries files needed to develop programs that use lvm2.

%package help
Summary:   Including man files for lvm2
Requires:  man
BuildArch: noarch

%description help
This contains man files for the using of lvm2.

%package -n python3-lvm-deprecated
Summary: Python 3 api to lvm
License: LGPLv2
Provides: python3-lvm = %{?epoch}:%{version}-%{release}
%{?python_provide:%python_provide python3-lvm}
Provides: %{name}-python3-libs = %{?epoch}:%{version}-%{release}
Obsoletes: %{name}-python3-libs < %{?epoch}:%{version}-%{release}
Requires: %{name}-libs = %{?epoch}:%{version}-%{release}

%description -n python3-lvm-deprecated
Support python 3 to use lvm.

%if %{use_lockd_dlm} || %{use_lockd_sanlock}
%package lockd
Summary:  LVM locking daemon
Requires: lvm2 = %{?epoch}:%{version}-%{release}
%if %{use_lockd_sanlock}
Requires: sanlock-lib >= %{sanlock_version}
%endif
%if %{use_lockd_dlm}
Requires: dlm-lib >= %{dlm_version}
%endif
Requires(post):   systemd-units >= %{systemd_version}
Requires(preun):  systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

%description lockd
LVM commands use lvmlockd to coordinate access to shared storage.
%endif

%if %{use_cluster}
%package cluster
Summary:  cluster LVM daemon tools
License:  GPLv2
Requires: lvm2 = %{?epoch}:%{version}-%{release}
Requires(preun): device-mapper >= %{?epoch}:%{device_mapper_version}
Requires(preun): lvm2 >= 2.02
Requires:  corosync >= %{corosync_version}
Requires:  dlm >= %{dlm_version}
Requires:  resource-agents >= %{resource_agents_version}
Provides:  cluster-standalone
Obsoletes: cluster-standalone

%description cluster
cluster distributes LVM metadata updates  around  a  cluster.
%endif

%if %{use_cluster} && %{use_cmirror}
%package -n cmirror
Summary:   cluster mirror log daemon
License:   GPLv2
Requires:  corosync >= %{corosync_version}
Requires:  device-mapper = %{?epoch}:%{device_mapper_version}-%{release}
Requires:  resource-agents >= %{resource_agents_version}
Provides:  cmirror-standalone
Obsoletes: cmirror-standalone

%description -n cmirror
cmirror tracks mirror log information in a cluster.
%endif

%package dbusd
Summary:  LVM2 D-Bus daemon
License:  GPLv2
Requires: lvm2 >= %{?epoch}:%{version}-%{release}
Requires: dbus
Requires: python3-dbus
Requires: python3-pyudev
Requires: python3-gobject-base
Requires(post):   systemd-units >= %{systemd_version}
Requires(preun):  systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

%description dbusd
dbusd is a service which provides a D-Bus API to the logical volume manager.

%package test
Summary:   Testsuite for lvm2
License:   LGPLv2 and GPLv2 and BSD-2-Clause
Provides:  %{name}-testsuite
Obsoletes: %{name}-testsuite

%description test
An extensive functional testsuite for LVM2.

%prep
%autosetup -n LVM2.%{version} -p1

%package -n device-mapper
Summary:   Low level logical volume management
Version:   %{device_mapper_version}
License:   LGPLv2
URL:       http://sources.redhat.com/dm
Requires:  util-linux >= %{util_linux_version}
Requires:  systemd >= %{systemd_version}
Provides:  device-mapper-libs = %{?epoch}:%{device_mapper_version}-%{release}
Obsoletes: device-mapper-libs
Conflicts: dracut < %{dracut_version}

%description -n device-mapper
Manages logical devices that use the device-mapper driver.

%package -n device-mapper-event
Summary:   Handle device-mapper events
Version:   %{device_mapper_version}
Requires:  device-mapper = %{?epoch}:%{device_mapper_version}-%{release}
Requires:  systemd-units
Provides:  device-mapper-event-libs = %{?epoch}:%{device_mapper_version}-%{release}
Obsoletes: device-mapper-event-libs

%description -n device-mapper-event
It contains tthe event monitoring daemon for device-mapper devices.  Library plugins
can register and carryout actions triggered when particular events occur.

%build
%configure --with-default-dm-run-dir=/run --with-default-run-dir=/run/lvm --with-default-pid-dir=/run --with-default-locking-dir=/run/lock/lvm --with-usrlibdir=%{_libdir} --enable-fsadm --enable-write_install --with-user= --with-group= --with-device-uid=0 --with-device-gid=6 --with-device-mode=0660 --enable-pkgconfig --enable-applib --enable-cmdlib --enable-dmeventd --enable-blkid_wiping %{?configure_cluster} %{?configure_cmirror} --with-udevdir=%{_prefix}/lib/udev/rules.d --enable-udev_sync --with-thin=internal --with-thin=internal --enable-lvmpolld %{?configure_lockd_dlm} %{?configure_lockd_sanlock} --enable-dbus-service --enable-notify-dbus --enable-dmfilemapd
make %{?_smp_mflags}

%check
make run-unit-test

%install
make install DESTDIR=%{buildroot}
make install_system_dirs DESTDIR=%{buildroot}
make install_systemd_units DESTDIR=%{buildroot}
make install_systemd_generators DESTDIR=%{buildroot}
make install_tmpfiles_configuration DESTDIR=%{buildroot}
make -C test install DESTDIR=%{buildroot}

%post
/sbin/ldconfig
%systemd_post blk-availability.service lvm2-monitor.service
if [ "$1" = "1" ] ; then
    systemctl enable lvm2-monitor.service
    systemctl start lvm2-monitor.service >/dev/null 2>&1 || :
fi

%systemd_post lvm2-lvmpolld.socket
systemctl enable lvm2-lvmpolld.socket
systemctl start lvm2-lvmpolld.socket >/dev/null 2>&1 || :

%preun
%systemd_preun blk-availability.service lvm2-monitor.service
%systemd_preun lvm2-lvmpolld.service lvm2-lvmpolld.socket

%postun
%systemd_postun lvm2-monitor.service
%systemd_postun_with_restart lvm2-lvmpolld.service
/sbin/ldconfig

%post -n device-mapper
/sbin/ldconfig

%postun -n device-mapper
/sbin/ldconfig

%post -n device-mapper-event
/sbin/ldconfig
%systemd_post dm-event.socket
systemctl enable dm-event.socket
systemctl start dm-event.socket >/dev/null 2>&1 || :
if [ -e %{_default_pid_dir}/dmeventd.pid ]; then
    %{_sbindir}/dmeventd -R || echo "Failed to start dmeventd."
fi

%preun -n device-mapper-event
%systemd_preun dm-event.service dm-event.socket

%postun -n device-mapper-event
/sbin/ldconfig

%if %{use_lockd_dlm} || %{use_lockd_sanlock}
%post lockd
%systemd_post lvmlockd.service lvmlocks.service
%preun lockd
%systemd_preun lvmlockd.service lvmlocks.service
%postun lockd
%systemd_postun lvmlockd.service lvmlocks.service 
%endif

%if %{use_cluster}
%post cluster
if [ -e /run/clvmd.pid ]; then
    /usr/sbin/clvmd -S || echo "Failed to start clvmd."
fi
%systemd_post lvm2-clvmd.service lvm2-cluster-activation.service

%preun cluster
if [ "$1" = "0" ]; then
    /sbin/lvmconf --disable-cluster
fi
%systemd_preun lvm2-clvmd.service lvm2-cluster-activation.service

%postun cluster
%systemd_postun lvm2-clvmd.service lvm2-cluster-activation.service
%endif

%if %{use_cluster} && %{use_cmirror}
%post -n cmirror
%systemd_post lvm2-cmirrord.service

%preun -n cmirror
%systemd_preun lvm2-cmirrord.service

%postun -n cmirror
%systemd_postun lvm2-cmirrord.service
%endif

%post dbusd
%systemd_post lvm2-lvmdbusd.service

%preun dbusd
%systemd_preun lvm2-lvmdbusd.service

%postun dbusd
%systemd_postun lvm2-lvmdbusd.service

%files
%license COPYING COPYING.LIB

%defattr(555,root,root,-)
%{_sbindir}/fsadm
%{_sbindir}/lvm
%{_sbindir}/lvmconfig
%{_sbindir}/lvmdump
%{_sbindir}/lvmpolld
%{_libdir}/liblvm2cmd.so.*
%{_libdir}/libdevmapper-event-lvm2.so.*

%defattr(444,root,root,-)
%{_sbindir}/lvchange
%{_sbindir}/lvconvert
%{_sbindir}/lvcreate
%{_sbindir}/lvdisplay
%{_sbindir}/lvextend
%{_sbindir}/lvmdiskscan
%{_sbindir}/lvmsadc
%{_sbindir}/lvmsar
%{_sbindir}/lvreduce
%{_sbindir}/lvremove
%{_sbindir}/lvrename
%{_sbindir}/lvresize
%{_sbindir}/lvs
%{_sbindir}/lvscan
%{_sbindir}/pv*
%{_sbindir}/vg*
%{_sbindir}/lvmdevices
%{_sbindir}/lvm_import_vdo

%{_prefix}/lib/udev/rules.d/69-dm-lvm.rules
%{_prefix}/lib/udev/rules.d/11-dm-lvm.rules

%dir %{_sysconfdir}/lvm
%ghost %{_sysconfdir}/lvm/cache/.cache
%attr(644, -, -) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvm.conf
%attr(644, -, -) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvmlocal.conf
%dir %{_sysconfdir}/lvm/profile
%{_sysconfdir}/lvm/profile/*
%dir %{_sysconfdir}/lvm/backup
%dir %{_sysconfdir}/lvm/cache
%dir %{_sysconfdir}/lvm/archive
%ghost %dir /run/lock/lvm
%ghost %dir /run/lvm
%dir %{_libdir}/device-mapper
%{_libdir}/device-mapper/*
%{_libdir}/libdevmapper-event-lvm2mirror.so
%{_libdir}/libdevmapper-event-lvm2snapshot.so
%{_libdir}/libdevmapper-event-lvm2raid.so
%{_libdir}/libdevmapper-event-lvm2thin.so
%{_libdir}/libdevmapper-event-lvm2vdo.so
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-monitor.service
%{_unitdir}/lvm2-lvmpolld.socket
%{_unitdir}/lvm2-lvmpolld.service

%files -n device-mapper
%license COPYING COPYING.LIB
%doc udev/12-dm-permissions.rules
%defattr(555,root,root,-)
%{_sbindir}/dmsetup
%{_sbindir}/blkdeactivate
%{_sbindir}/dmstats
%{_sbindir}/dmfilemapd
%{_libdir}/libdevmapper.so.*
%defattr(444,root,root,-)
%{_prefix}/lib/udev/rules.d/10-dm.rules
%{_prefix}/lib/udev/rules.d/13-dm-disk.rules
%{_prefix}/lib/udev/rules.d/95-dm-notify.rules

%files -n device-mapper-event
%license COPYING.LIB
%defattr(555,root,root,-)
%{_sbindir}/dmeventd
%{_libdir}/libdevmapper-event.so.*
%defattr(444,root,root,-)
%{_unitdir}/dm-event.socket
%{_unitdir}/dm-event.service

%files devel
%defattr(444,root,root,-)
%{_libdir}/liblvm2cmd.so
%{_libdir}/libdevmapper-event-lvm2.so
%{_libdir}/libdevmapper.so
%{_libdir}/libdevmapper-event.so
%{_includedir}/lvm2cmd.h
%{_includedir}/libdevmapper.h
%{_includedir}/libdevmapper-event.h
%{_libdir}/pkgconfig/devmapper.pc
%{_libdir}/pkgconfig/devmapper-event.pc

%files help
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%if %{use_lockd_dlm} || %{use_lockd_sanlock}
%files lockd
%defattr(444,root,root,-)
%%attr(555, -, -) %{_sbindir}/lvmlockd
%%attr(555, -, -) %{_sbindir}/lvmlockctl
%{_unitdir}/lvmlockd.service
%{_unitdir}/lvmlocks.service
%endif

%if %{use_cluster}
%files cluster
%defattr(555,root,root,-)
%{_sbindir}/clvmd
%{_prefix}/lib/systemd/lvm2-cluster-activation
%defattr(444,root,root,-)
%{_unitdir}/lvm2-clvmd.service
%{_unitdir}/lvm2-cluster-activation.service
%endif

%if %{use_cluster} && %{use_cmirror}
%files -n cmirror
%defattr(555,root,root,-)
%{_sbindir}/cmirrord
%{_unitdir}/lvm2-cmirrord.service
%endif

%files dbusd
%defattr(555,root,root,-)
%{_sbindir}/lvmdbusd
%defattr(444,root,root,-)
%{_sysconfdir}/dbus-1/system.d/com.redhat.lvmdbus1.conf
%{_datadir}/dbus-1/system-services/com.redhat.lvmdbus1.service
%{_unitdir}/lvm2-lvmdbusd.service
%{python3_sitelib}/lvmdbusd/*

%files test
%license COPYING COPYING.LIB COPYING.BSD
%{_datadir}/lvm2-testsuite/
%{_libexecdir}/lvm2-testsuite/
%{_bindir}/lvm2-testsuite


%changelog
* Sat Oct 15 2022 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.16-1
- upgrade version to 2.03.16 

* Tue Oct 11 2022 miaoguanqin <miaoguanqin@huawei.com> - 8:2.03.14-7
- lvm: remove no locking warning

* Sun Sep 04 2022 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.14-6
- lvm: fix segfault of pvscan --cache

* Wed Apr 27 2022 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.14-5
- lvm: fix error of epoch version

* Sun Jan 30 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 8:2.03.14-4
- lvm: code reduce cyclomatic complexity

* Sun Jan 30 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 8:2.03.14-3
- dev_name() determine whether the dev->aliases linked list is
 empty before obtaining the dev name

* Sun Jan 30 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 8:2.03.14-2
- check DM_NAME before creating symlink in 13-dm-disk.rules

* Mon Nov 22 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.14-1
- upgrade to 2.03.14

* Mon Nov 08 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-6
- add device-mapper-event to solve the problem of compilation error

* Wed Jul 28 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-5
- %check modified to make run-unit-test 

* Wed Jul 28 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-4
- lvreduce support --yes option

* Mon Jul 26 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-3
- revert commit of fix VERSION issue when packaging

* Fri Jul 23 2021 zhouwenpei <zhouwenpei1@huawei.com> - 8:2.03.11-2
- remove unnecessary build require.

* Thu Jan 28 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-1
- update lvm2 version to 2.03.11

* Wed Dec 23 2020 yanglongkang <yanglongkang@huawei.com> - 8:2.03.09-5
- backport upstream patches-epoch2 to fix some problems

* Wed Nov 4 2020 lixiaokeng <lixiaokeng@huawei.com> - 8:2.03.09-4
- add make test

* Thu Aug 6 2020 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.09-3
- update master branch device-mapper-version more than LTS branch
 
* Fri Jul 24 2020 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.09-2
- update device-mapper-version to 1.02.151

* Tue Jul 14 2020 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.09-1
- update lvm2 version to 2.03.09-1


* Thu Jul 2 2020 Wu Bo <wubo009@163.com> - 8:2.02.181-9
- rebuild package

* Fri Mar 20 2020 hy-euler <eulerstoragemt@huawei.com> - 8:2.02.181-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: the building requires the gdb

* Wed Mar 11 2020 wangjufeng <wangjufeng@huawei.com> - 8:2.02.181-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix heap memory leak

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix VERSION issue when packaging

* Sat Dec 28 2019 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync bugfix from community

* Mon Dec 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync bugfix from community

* Sat Nov 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-3
- Type:NA
- ID:NA
- SUG:NA
- DESC:remove some buildrequires in spec

* Fri Sep 06 2019 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-2
- Package init
