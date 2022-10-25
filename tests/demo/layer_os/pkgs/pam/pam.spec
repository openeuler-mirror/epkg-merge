%define _pamlibdir %{_libdir}
%define _moduledir %{_libdir}/security
%define _secconfdir %{_sysconfdir}/security
%define _pamconfdir %{_sysconfdir}/pam.d
Name: pam
Version: 1.5.2
Release: 2
Summary: Pluggable Authentication Modules for Linux
License: BSD and GPLv2+
URL: http://www.linux-pam.org/
Source0: https://github.com/linux-pam/linux-pam/releases/download/v%{version}/Linux-PAM-%{version}.tar.xz
Source1: https://github.com/linux-pam/linux-pam/releases/download/v%{version}/Linux-PAM-%{version}.tar.xz.asc
Source5: other.pamd
Source6: system-auth.pamd
Source7: password-auth.pamd
Source10: config-util.pamd
Source15: pamtmp.conf
Source16: postlogin.pamd
Source18: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

Provides: %{name}-sm3 = %{version}-%{release}

Patch1: bugfix-pam-1.1.8-faillock-systemtime.patch
Patch9000:openEuler-change-ndbm-to-gdbm.patch
Patch9001:0001-bugfix-cannot-open-database-file.patch
Patch9002:add-sm3-crypt-support.patch

BuildRequires: autoconf automake libtool bison flex sed cracklib-devel gdbm-devel
BuildRequires: perl-interpreter pkgconfig gettext-devel libtirpc-devel libnsl2-devel
BuildRequires: audit-libs-devel libselinux-devel

Requires: cracklib libpwquality coreutils glibc audit-libs libselinux libxcrypt-sm3

%description
PAM (Pluggable Authentication Modules) is a system of libraries that
handle the authentication tasks of applications (services) on the system.

%package devel
Summary: Development files for Linux-PAM
Requires: pam = %{version}-%{release}

%description devel
%{summary}.

%package help
Summary: Man pages for Linux-PAM
BuildArch: noarch

%description help
%{summary}.

%prep
%autosetup -n Linux-PAM-%{version} -p1
cp %{SOURCE18} .
autoreconf -i

%build
%configure \
	--disable-rpath \
	--libdir=%{_pamlibdir} \
	--includedir=%{_includedir}/security \
	--disable-static \
	--disable-prelude \
	--enable-db=ndbm

make -C po update-gmo
%make_build

%install
%make_install

mkdir -p doc/README.d
for readme in modules/pam_*/README ; do
        cp -f ${readme} doc/README.d/README.`dirname ${readme} | sed -e 's@^modules/@@'`
done

ln -sf pam_sepermit.so $RPM_BUILD_ROOT%{_moduledir}/pam_selinux_permit.so

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/Linux-PAM
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/environment

install -d -m 755 $RPM_BUILD_ROOT%{_pamconfdir}

install -m 644 -D modules/pam_namespace/pam_namespace.service \
  %{buildroot}%{_unitdir}/pam_namespace.service

install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_pamconfdir}/other
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_pamconfdir}/system-auth
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_pamconfdir}/password-auth
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_pamconfdir}/config-util
install -m 644 %{SOURCE16} $RPM_BUILD_ROOT%{_pamconfdir}/postlogin
install -m 600 /dev/null $RPM_BUILD_ROOT%{_secconfdir}/opasswd
install -d -m 755 $RPM_BUILD_ROOT/var/log
install -m 600 /dev/null $RPM_BUILD_ROOT/var/log/tallylog
install -d -m 755 $RPM_BUILD_ROOT/var/run/faillock

for phase in auth acct passwd session ; do
	ln -sf pam_unix.so $RPM_BUILD_ROOT%{_moduledir}/pam_unix_${phase}.so 
done

install -m644 -D %{SOURCE15} $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/pam.conf

find $RPM_BUILD_ROOT -type f -name "*.la" -delete -print
rm -fr $RPM_BUILD_ROOT/usr/share/doc/pam

%find_lang Linux-PAM

%check
make check

%post
/sbin/ldconfig
if [ ! -e /var/log/tallylog ] ; then
	/usr/bin/install -m 600 /dev/null /var/log/tallylog || :
fi

%postun -p /sbin/ldconfig

%files -f Linux-PAM.lang
%defattr(-,root,root)
%license Copyright COPYING gpl-2.0.txt 
%doc AUTHORS README ChangeLog NEWS
%doc doc/README.d/
%dir %{_pamconfdir}
%config(noreplace) %{_pamconfdir}/other
%config(noreplace) %{_pamconfdir}/system-auth
%config(noreplace) %{_pamconfdir}/password-auth
%config(noreplace) %{_pamconfdir}/config-util
%config(noreplace) %{_pamconfdir}/postlogin
%{_pamlibdir}/libpam.so.*
%{_pamlibdir}/libpamc.so.*
%{_pamlibdir}/libpam_misc.so.*
%attr(4755,root,root) %{_sbindir}/pam_timestamp_check
%attr(4755,root,root) %{_sbindir}/unix_chkpwd
%attr(0700,root,root) %{_sbindir}/unix_update
%attr(0755,root,root) %{_sbindir}/pwhistory_helper
%{_sbindir}/faillock
%{_sbindir}/mkhomedir_helper
%{_sbindir}/pam_namespace_helper
%attr(0755,root,root) %{_sbindir}/pam_namespace_helper
%dir %{_moduledir}
%{_moduledir}/pam*.so
%{_moduledir}/pam_filter/
%{_unitdir}/pam_namespace.service
%dir %{_secconfdir}
%config(noreplace) %{_secconfdir}/access.conf
%config(noreplace) %{_secconfdir}/group.conf
%config(noreplace) %{_secconfdir}/limits.conf
%dir %{_secconfdir}/limits.d
%config(noreplace) %{_secconfdir}/namespace.conf
%dir %{_secconfdir}/namespace.d
%attr(755,root,root) %config(noreplace) %{_secconfdir}/namespace.init
%config(noreplace) %{_secconfdir}/pam_env.conf
%config(noreplace) %{_secconfdir}/time.conf
%config(noreplace) %{_secconfdir}/opasswd
%config(noreplace) %{_secconfdir}/sepermit.conf
%config(noreplace) %{_secconfdir}/faillock.conf
%dir /var/run/sepermit
%ghost %verify(not md5 size mtime) /var/log/tallylog
%dir /var/run/faillock
%{_prefix}/lib/tmpfiles.d/pam.conf

%files devel
%defattr(-,root,root)
%{_includedir}/security
%{_libdir}/libpam.so
%{_libdir}/libpamc.so
%{_libdir}/libpam_misc.so
%{_libdir}/pkgconfig/pam.pc
%{_libdir}/pkgconfig/pam_misc.pc
%{_libdir}/pkgconfig/pamc.pc

%files help
%defattr(-,root,root)
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*


%changelog
* Fri Jan 14 2022 wangyu <wangyu283@huawei.com> - 1.5.2-2
- add sm3 crypt support

* Mon Dec 27 2021 yuanxin <yuanxin24@huawei.com> - 1.5.2-1
- update version to 1.5.2

* Wed Nov 10 2021 renhongxun <renhongxun@huawei.com> - 1.5.1-5
- cleancode

* Wed Sep 15 2021 chenyaqiang <chenyaqiang@huawei.com> - 1.5.1-4
- bugfix with cannot open database file

* Thu Jul 15 2021 shixuantong <shixuantong@huawei.com> - 1.5.1-3
- remove unnecessary dependency packages from the spec file

* Fri Jul 9 2021 shangyibin <shangyibin1@huawei.com> - 1.5.1-2
- use gdbm

* Sat Jan 23 2021 panxiaohe <panxiaohe@huawei.com> - 1.5.1-1
- update to 1.5.1

* Sat Oct 31 2020 panxiaohe <panxiaohe@huawei.com> - 1.4.0-3
- Prevent SEGFAULT for unknown UID

* Fri Sep 25 2020 panxiaohe <panxiaohe@huawei.com> - 1.4.0-2
- backport some patches from upstream

* Fri Jul 24 2020 Liquor <lirui130@huawei.com> - 1.4.0-1
- update to 1.4.0

* Wed Jun 17 2020 Liquor <lirui130@huawei.com> - 1.3.1-9
- fix login message

* Sun Jan 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.3.1-8
- update config

* Fri Jan 10 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.3.1-7
- clean code

* Mon Dec 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.3.1-6
- Modify man

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.3.1-5
- Adjust requires

* Sat Sep 14 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.3.1-4
- Package init
