%define compldir %{_datadir}/bash-completion/completions/
%global upstream_major 2.37

Name:           util-linux
Version:        2.37.2
Release:        5
Summary:        A random collection of Linux utilities
License:        GPLv2 and GPLv2+ and LGPLv2+ and BSD with advertising and Public Domain
URL:            https://git.kernel.org/pub/scm/utils/util-linux/util-linux.git
Source0:        https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v%{upstream_major}/%{name}-%{version}.tar.xz
Source1:        util-linux-login.pamd
Source2:        util-linux-remote.pamd
Source3:        util-linux-chsh-chfn.pamd
Source4:        util-linux-60-raw.rules
Source5:        adjtime
Source6:        util-linux-su.pamd
Source7:        util-linux-su-l.pamd
Source8:        util-linux-runuser.pamd
Source9:        util-linux-runuser-l.pamd

Patch0:         2.36-login-lastlog-create.patch
Patch1:         Add-check-to-resolve-uname26-version-test-failed.patch
Patch2:         SKIPPED-no-root-permissions-test.patch
Patch3:         backport-su-bash-completion-offer-usernames-rather-than-files.patch
Patch4:         backport-Fix-memory-leaks-in-the-chcpu.patch
Patch5:         backport-logger-fix-prio-prefix-doesn-t-use-priority-default.patch
Patch6:         backport-vipw-flush-stdout-before-getting-answer.patch  
Patch7:         backport-login-Restore-tty-size-after-calling-vhangup.patch
Patch8:         backport-Forward-value-of-sector_size-instead-of-its-address.patch
Patch9:         backport-libfdisk-dereference-of-possibly-NULL-gcc-analyzer.patch
Patch10:        backport-libfdisk-check-calloc-return-gcc-analyzer.patch
Patch11:        backport-mcookie-fix-infinite-loop-when-use-f.patch
Patch12:        backport-sfdisk-write-empty-label-also-when-only-ignored-part.patch

BuildRequires:  audit-libs-devel >= 1.0.6 gettext-devel libselinux-devel ncurses-devel pam-devel zlib-devel popt-devel
BuildRequires:  libutempter-devel systemd-devel systemd libuser-devel libcap-ng-devel python3-devel gcc

Requires(post): coreutils
Requires:       pam >= 1.1.3-7, /etc/pam.d/system-auth audit-libs >= 1.0.6
Requires:       libblkid = %{version}-%{release} libmount = %{version}-%{release} libsmartcols = %{version}-%{release}
Requires:       libfdisk = %{version}-%{release} libuuid = %{version}-%{release} 

Conflicts:      initscripts < 9.79-4 bash-completion < 1:2.1-1 coreutils < 8.20 sysvinit-tools < 2.88-14
Conflicts:      e2fsprogs < 1.41.8-5 filesystem < 3

Provides:       eject = 2.1.6 rfkill = 0.5
Provides:       util-linux-ng = %{version}-%{release} hardlink = 1:1.3-9
Provides:       /bin/dmesg /bin/kill /bin/more /bin/mount /bin/umount /sbin/blkid
Provides:       /sbin/blockdev /sbin/findfs /sbin/fsck /sbin/nologin
Obsoletes:      eject <= 2.1.5 rfkill <= 0.5 util-linux-ng < 2.19 hardlink <= 1:1.3-9

%description
The util-linux package contains a random collection of files that
implements some low-level basic linux utilities.

%package -n libfdisk
Summary: Library for fdisk-like programs.
License: LGPLv2+

%description -n libfdisk
This package contains the library for fdisk-like programs.

%package -n libsmartcols
Summary: Library for column based text sort engine.
License: LGPLv2+

%description -n libsmartcols
This package contains the library for column based text sort engine.

%package -n libmount
Summary: Library for device mounting
License: LGPLv2+
Requires: libblkid = %{version}-%{release}
Requires: libuuid = %{version}-%{release}
Conflicts: filesystem < 3

%description -n libmount
This package is the library for device mounting.

%package -n libblkid
Summary: Library for block device id.
License: LGPLv2+
Requires: libuuid = %{version}-%{release}
Conflicts: filesystem < 3
Requires(post): coreutils

%description -n libblkid
This package is le library for block device id.

%package -n uuidd
Summary:  UUID generation daemon
Requires: libuuid = %{version}-%{release}
License: GPLv2
Requires: systemd
Requires(pre): shadow
Requires(post): systemd-units
Requires(preun): systemd-units

%description -n uuidd
The uuidd daemon is used by the UUID library to generate universally
unique identifiers (UUIDs), especially time-based UUIDs, in a secure
and guaranteed-unique fashion, even in the face of large numbers of
threads running on different CPUs trying to grab UUIDs.

%package -n libuuid
Summary: Universally unique ID library
License: BSD
Conflicts: filesystem < 3

%description -n libuuid
This package is the universally unique ID library.

%package user
Summary: libuser based util-linux utilities
License: GPLv2
Requires: util-linux = %{version}-%{release}

%description user
chfn and chsh utilities with dependence on libuser

%package -n python3-libmount
Summary:        Python Package for the libmount library pack
Requires:       libmount = %{version}-%{release}
License:        LGPLv2+

%description -n python3-libmount
This package provides python support for users to use the libmount library
to work with mount tables and mount filesystems.

%package devel
Summary:        Development package for ${name}
License:        LGPLv2+ and BSD
Requires:       %{name} = %{version}-%{release} pkgconfig
Provides:       libfdisk-devel libsmartcols-devel libmount-devel libblkid-devel libuuid-devel
Obsoletes:      libfdisk-devel libsmartcols-devel libmount-devel libblkid-devel libuuid-devel

%description devel
This package contains some library and other necessary files for the
development of %{name}.

%package help
Summary:        Help package for ${name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Obsoletes:      hardlink-help <= 1:1.3-9
Provides:       hardlink-help = 1:1.3-9

%description help
This package contains some doc and man help files for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%define _build_arg0__ CFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 $RPM_OPT_FLAGS" SUID_CFLAGS="-fpie"
%define _build_arg1__ SUID_LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now" DAEMON_CFLAGS="$SUID_CFLAGS" DAEMON_LDFLAGS="$SUID_LDFLAGS"

unset LINGUAS || :
%configure \
  --with-systemdsystemunitdir=%{_unitdir} \
  --disable-silent-rules \
  --disable-bfs \
  --disable-pg \
  --enable-chfn-chsh \
  --enable-usrdir-path \
  --enable-write \
  --enable-raw \
  --enable-hardlink \
  --with-python=3 \
  --with-systemd \
  --with-udev \
  --with-selinux \
  --with-audit \
  --with-utempter \
  --disable-makeinstall-chown

%make_build %{_build_arg0__} %{_build_arg1__}

%check
make check

%install
%make_install

install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}{/run/uuidd,/var/lib/libuuid,/var/log}

mv %{buildroot}%{_sbindir}/raw %{buildroot}%{_bindir}/raw
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/login
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/remote
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/chsh
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/chfn
install -Dm644 %{SOURCE4} %{buildroot}%{_prefix}/lib/udev/rules.d/60-raw.rules
install -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/adjtime
install -m644 %{SOURCE6} %{buildroot}%{_sysconfdir}/pam.d/su
install -m644 %{SOURCE7} %{buildroot}%{_sysconfdir}/pam.d/su-l
install -m644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/runuser
install -m644 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/runuser-l

ln -sf hwclock %{buildroot}%{_sbindir}/clock
ln -sf ../proc/self/mounts %{buildroot}/etc/mtab

touch %{buildroot}/var/log/lastlog
chmod 0644 %{buildroot}/var/log/lastlog

echo ".so man8/raw.8" > %{buildroot}%{_mandir}/man8/rawdevices.8
echo ".so man8/hwclock.8" > %{buildroot}%{_mandir}/man8/clock.8

%find_lang %name

find  %{buildroot}%{_bindir}/ -regextype posix-egrep -type l \
  -regex ".*(linux32|linux64|aarch64|i386|x86_64|uname26)$" \
  -printf "%{_bindir}/%f\n" > %{name}.files
cat %{name}.lang >> %{name}.files

find  %{buildroot}%{_mandir}/man8 -regextype posix-egrep  \
  -regex ".*(linux32|linux64|aarch64|i386|x86_64|uname26)\.8.*" \
  -printf "%{_mandir}/man8/%f*\n" > %{name}-help.files

rm -rf %{buildroot}%{_libdir}/*.{la,a}
rm -rf %{buildroot}%{_libdir}/python*/site-packages/*.{la,a}

%pre -n uuidd
getent group uuidd >/dev/null || groupadd -r uuidd
getent passwd uuidd >/dev/null || \
useradd -r -g uuidd -d /var/lib/libuuid -s /sbin/nologin \
    -c "UUID generator helper daemon" uuidd
exit 0

%post
[ -d /var/log ] || mkdir -p /var/log

touch /var/log/lastlog
chown root:root /var/log/lastlog
chmod 0644 /var/log/lastlog

if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled
then
    SECXT=`/usr/sbin/matchpathcon -n /var/log/lastlog 2> /dev/null`
    if [ -n "$SECXT" ]
    then
        /usr/bin/chcon "$SECXT"  /var/log/lastlog >/dev/null 2>&1 || :
    fi
fi
if [ ! -L /etc/mtab ]
then
    ln -sf ../proc/self/mounts /etc/mtab || :
fi

%post -n libblkid 
/sbin/ldconfig

[ -d /run/blkid ] || mkdir -p /run/blkid
for i in /etc/blkid.tab /etc/blkid.tab.old \
  /etc/blkid/blkid.tab /etc/blkid/blkid.tab.old
do
    if [ -f "${i}" ]
    then
        mv "${i}" /run/blkid/ || :
    fi
done

%postun -n libblkid -p /sbin/ldconfig

%post -n libuuid -p /sbin/ldconfig
%postun -n libuuid -p /sbin/ldconfig

%post -n libmount -p /sbin/ldconfig
%postun -n libmount -p /sbin/ldconfig

%post -n libsmartcols -p /sbin/ldconfig
%postun -n libsmartcols -p /sbin/ldconfig

%post -n libfdisk -p /sbin/ldconfig
%postun -n libfdisk -p /sbin/ldconfig

%post -n uuidd
%systemd_post uuidd
if [ $1 -eq 1 ]
then
    /bin/systemctl start uuidd > /dev/null 2>&1 || :
fi

%preun -n uuidd
%systemd_preun uuidd

%postun -n uuidd
/sbin/ldconfig
%systemd_postun_with_restart uuidd

%files -f %{name}.files
%exclude %{compldir}/{mount,umount}
%{!?_licensedir:%global license %%doc}
%license Documentation/licenses/* AUTHORS
%config(noreplace) %{_sysconfdir}/pam.d/{login,remote,su,su-l,runuser,runuser-l}
%config(noreplace) %{_prefix}/lib/udev/rules.d/60-raw.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adjtime
%attr(4755,root,root) %{_bindir}/mount
%attr(4755,root,root) %{_bindir}/umount
%attr(4755,root,root) %{_bindir}/su
%attr(755,root,root) %{_bindir}/login
%attr(2755,root,tty) %{_bindir}/write
%attr(2555,root,tty) %{_bindir}/wall
%ghost %attr(0644,root,root) %verify(not md5 size mtime) /var/log/lastlog
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) /etc/mtab
%{_unitdir}/fstrim.*
%{_bindir}/{cal,chrt,col,colcrt,colrm,column,chmem,dmesg,eject,fallocate,fincore,findmnt,choom,uclampset}
%{_bindir}/{flock,getopt,hexdump,ionice,ipcmk,ipcrm,ipcs,isosize,kill,last,lastb,logger,hardlink}
%{_bindir}/{look,lsblk,lscpu,lsipc,lslocks,lslogins,lsmem,lsns,mcookie,mesg,more,mountpoint}
%{_bindir}/{namei,nsenter,prlimit,raw,rename,renice,rev,script,scriptreplay,setarch,setpriv}
%{_bindir}/{setsid,setterm,taskset,ul,unshare,utmpdump,uuidgen,uuidparse,wdctl,whereis,scriptlive,irqtop,lsirq}
%{_sbindir}/{addpart,agetty,blkdiscard,blkid,blkzone,blockdev,chcpu,ctrlaltdel,delpart,fdisk}
%{_sbindir}/{findfs,fsck,fsck.cramfs,fsck.minix,fsfreeze,fstrim,ldattach,losetup,mkfs,mkfs.cramfs}
%{_sbindir}/{mkfs.minix,mkswap,nologin,partx,pivot_root,readprofile,resizepart,rfkill,rtcwake}
%{_sbindir}/{runuser,sulogin,swaplabel,swapoff,swapon,switch_root,wipefs,zramctl}
%{_sbindir}/{clock,fdformat,hwclock,cfdisk,sfdisk}
%{compldir}/{addpart,blkdiscard,blkid,blkzone,blockdev,cal,chcpu,chmem,chrt,col}
%{compldir}/{colcrt,colrm,column,ctrlaltdel,delpart,dmesg,eject,fallocate,fdisk}
%{compldir}/{fincore,findfs,findmnt,flock,fsck,fsck.cramfs,fsck.minix,fsfreeze}
%{compldir}/{fstrim,getopt,hexdump,ionice,ipcmk,ipcrm,ipcs,isosize,last,ldattach}
%{compldir}/{logger,look,losetup,lsblk,lscpu,lsipc,lslocks,lslogins,lsmem,lsns}
%{compldir}/{mcookie,mesg,mkfs,mkfs.cramfs,mkfs.minix,mkswap,more,mountpoint}
%{compldir}/{namei,nsenter,partx,pivot_root,prlimit,raw,readprofile,rename,renice}
%{compldir}/{resizepart,rev,rfkill,rtcwake,runuser,script,scriptreplay,setarch}
%{compldir}/{setpriv,setsid,setterm,su,swaplabel,swapoff,swapon,taskset,ul,unshare}
%{compldir}/{utmpdump,uuidgen,uuidparse,wall,wdctl,whereis,wipefs,write,zramctl}
%{compldir}/{fdformat,hwclock,cfdisk,sfdisk,scriptlive,irqtop,lsirq,hardlink,uclampset}

%files -n libfdisk
%license Documentation/licenses/COPYING.LGPL-2.1* libfdisk/COPYING
%{_libdir}/libfdisk.so.*

%files -n libsmartcols
%license Documentation/licenses/COPYING.LGPL-2.1* libsmartcols/COPYING
%{_libdir}/libsmartcols.so.*

%files -n libmount
%license Documentation/licenses/COPYING.LGPL-2.1* libmount/COPYING
%{_libdir}/libmount.so.*

%files -n libblkid
%doc libblkid/COPYING
%{_libdir}/libblkid.so.*

%files -n uuidd
%license Documentation/licenses/COPYING.GPL-2.0*
%{_sbindir}/uuidd
%{_unitdir}/uuidd.*
%dir %attr(2775, uuidd, uuidd) /var/lib/libuuid
%dir %attr(2775, uuidd, uuidd) /run/uuidd
%{compldir}/uuidd

%files -n libuuid
%license Documentation/licenses/COPYING.BSD-3* libuuid/COPYING
%{_libdir}/libuuid.so.*

%files user
%config(noreplace)	%{_sysconfdir}/pam.d/chfn
%config(noreplace)	%{_sysconfdir}/pam.d/chsh
%attr(4711,root,root)	%{_bindir}/chfn
%attr(4711,root,root)	%{_bindir}/chsh
%{compldir}/chfn
%{compldir}/chsh

%files -n python3-libmount
%{!?_licensedir:%global license %%doc}
%license libmount/COPYING
%{_libdir}/python*/site-packages/libmount/

%files devel
%{_includedir}/{libfdisk,libsmartcols,uuid,blkid,libmount}
%{_libdir}/{libfdisk.so,libsmartcols.so,libuuid.so,libblkid.so,libmount.so}
%{_libdir}/pkgconfig/{fdisk.pc,smartcols.pc,uuid.pc,blkid.pc,mount.pc}

%files help
%exclude %{_datadir}/doc/util-linux/getopt/*
%{_docdir}/%{name}/getopt-example.*
%doc README NEWS Documentation/deprecated.txt
%doc %attr(0644,-,-) misc-utils/getopt-*.{bash,tcsh}
%{_mandir}/man1/{chfn.1*,chsh.1*,cal.1*,chrt.1*,col.1*,colcrt.1*,colrm.1*,column.1*,dmesg.1*,eject.1*,uclampset.1*}
%{_mandir}/man1/{fallocate.1*,fincore.1*,flock.1*,getopt.1*,hexdump.1*,ionice.1*,ipcmk.1*,ipcrm.1*,ipcs.1*}
%{_mandir}/man1/{kill.1*,last.1*,lastb.1*,logger.1*,login.1*,look.1*,lscpu.1*,lsipc.1*,lslogins.1*,lsmem.1*}
%{_mandir}/man1/{mcookie.1*,mesg.1*,more.1*,mountpoint.1*,namei.1*,nsenter.1*,prlimit.1*,rename.1*,renice.1*}
%{_mandir}/man1/{rev.1*,runuser.1*,script.1*,scriptreplay.1*,setpriv.1*,setsid.1*,setterm.1*,su.1*,taskset.1*}
%{_mandir}/man1/{ul.1*,unshare.1*,utmpdump.1.gz,uuidgen.1*,uuidparse.1*,wall.1*,whereis.1*,write.1*,choom.1*,scriptlive*,hardlink.1*,irqtop.1*,lsirq.1*}
%{_mandir}/man3/{libblkid.3*,uuid.3*,uuid_clear.3*,uuid_compare.3*,uuid_copy.3*,uuid_generate.3*,uuid_generate_random.3*}
%{_mandir}/man3/{uuid_generate_time_safe.3*,uuid_is_null.3*,uuid_parse.3*,uuid_time.3*,uuid_unparse.3*,uuid_generate_time.3*}
%{_mandir}/man5/{fstab.5*,terminal-colors.d.5*,adjtime_config.5.*}
%{_mandir}/man8/{uuidd.8*,fdformat.8*,hwclock.8*,clock.8*,cfdisk.8*,sfdisk.8*,addpart.8*,agetty.8*}
%{_mandir}/man8/{blkdiscard.8*,blkid.8*,blkzone.8*,blockdev.8*,chcpu.8*,chmem.8*,ctrlaltdel.8*,delpart.8*}
%{_mandir}/man8/{fdisk.8*,findfs.8*,findmnt.8*,fsck.8*,fsck.cramfs.8*,fsck.minix.8*,fsfreeze.8*,fstrim.8*}
%{_mandir}/man8/{isosize.8*,ldattach.8*,losetup.8*,lsblk.8*,lslocks.8*,lsns.8*,mkfs.8*,mkfs.cramfs.8*}
%{_mandir}/man8/{mkfs.minix.8*,mkswap.8*,mount.8*,nologin.8*,partx.8*,pivot_root.8*,raw.8*,rawdevices.8*}
%{_mandir}/man8/{readprofile.8*,resizepart.8*,rfkill.8*,rtcwake.8*,setarch.8*,sulogin.8.gz,swaplabel.8*}
%{_mandir}/man8/{swapoff.8*,swapon.8*,switch_root.8*,umount.8*,wdctl.8.gz,wipefs.8*,zramctl.8*}

%changelog
* Wed Jun 29 2022 shangyibin <shangyibin1@h-partners.com> - 2.37.2-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fallback to move hexdump from util-linux to util-linux-devel
       Fallback solve yum failure because of files conflicts

* Mon Jun 20 2022 shangyibin <shangyibin1@h-partners.com> - 2.37.2-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync patches
       move hexdump from util-linux to util-linux-devel
       solve yum failure because of files conflicts

* Wed Jun 15 2022 shangyibin <shangyibin1@h-partners.com> - 2.37.2-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix test fail

* Thu Jun 09 2022 renhongxun<renhongxun@h-partners.com> - 2.37.2-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:move hardlink/uclampset completions from util-linux-help to util-linux

* Mon Dec 27 2021 tianwei <tianwei12@huawei.com> - 2.37.2-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 2.37.2

* Tue Aug 10 2021 shixuantong<shixuantong@huawei.com> - 2.36.1-5
- Type:CVE
- ID:CVE-2021-37600
- SUG:NA
- DESC:fix CVE-2021-37600

* Thu Jul 22 2021 shixuantong<shixuantong@huawei.com> - 2.36.1-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove gdb from BuildRequires

* Thu Mar 18 2021 wangchen <wangchen137@huawei.com> - 2.36.1-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:use /sys to read all block devices

* Mon Mar 1 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.36.1-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix heap-buffer-overflow in fdisk_partname

* Tue Jan 26 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.36.1-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 2.36.1

* Mon Jan 18 2021 Liquor <lirui130@huawei.com> - 2.36-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Remove pam_console dependency

* Thu Dec 17 2020 Liquor <lirui130@huawei.com> - 2.36-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Add check to resolve uname26-version test failed

* Sat Nov 28 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.36-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:have wall not write to non-ttys(#65412)

* Mon Nov 2 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.36-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 2.36

* Thu Oct 29 2020 Liquor <lirui130@huawei.com> - 2.35.2-4
- Type:requirement
- ID:NA
- SUG:NA
- DESC:remove python2

* Tue Sep 8 2020 wangchen <wangchen137@huawei.com> - 2.35.2-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify the URL of Source0

* Fri Aug 28 2020 yang_zhuang_zhuang <yangzhuangzhuang1@huawei.com> - 2.35.2-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix an issue that hardlink was packaged twice

* Thu Jul 23 2020 yang_zhuang_zhuang <yangzhuangzhuang1@huawei.com> - 2.35.2-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 2.35.2

* Mon Jun 29 2020 Liquor <lirui130@huawei.com> - 2.34-9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add misc-setarch test to "known_fail"

* Sun Mar 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.34-8
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:don not usr the hardlink by default

* Sun Mar 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.34-7
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:enable hardlink of configure

* Sat Mar 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.34-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:obsolete hardlink that has been merged into util-linux of 2.34

* Fri Mar 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.34-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Add an entry for the HiSilicon aarch64 part tsv110 and
       use official name for HiSilicon tsv110

* Thu Mar 5 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.34-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:fix the problem of one iso can't mount directly twice by default

* Fri Feb 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.34-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:enable check

* Tue Jan 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.34-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add subpackages

* Sun Jan 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.34-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 2.34

* Wed Jan 8 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.32.1-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:fix quit dialog for non-libreadline version

* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.32.1-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify source

* Thu Oct 10 2019 shenyangyang<shenyangyang4@huawei.com> - 2.32.1-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify license file

* Sat Sep 21 2019 huzhiyu<huzhiyu1@huawei.com> - 2.32.1-2
- Package init
