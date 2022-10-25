Name:     cronie
Version:  1.6.1
Release:  1
Summary:  Standard UNIX daemon crond
License:  GPLv2+ and ISC
URL:      https://github.com/cronie-crond/cronie
Source0:  https://github.com/cronie-crond/cronie/releases/download/cronie-%{version}/cronie-%{version}.tar.gz


Patch0: bugfix-cronie-systemd-alias.patch

BuildRequires:  automake
BuildRequires:  gcc systemd libselinux-devel pam-devel audit-libs-devel 

Requires:  libselinux pam crontabs
Requires(preun):  systemd
Requires(postun): systemd
Requires(post):   systemd coreutils sed

Provides: dailyjobs anacron %{name}-anacron %{name}-noanacron

Obsoletes: %{name}-anacron %{name}-noanacron

%description
Cronie contains the standard UNIX daemon crond that runs specified programs 
at scheduled times and related tools. It is based on the original cron and 
has security and configuration enhancements like the ability to use pam and SELinux.

%package help
Summary:  Man pages and other related documents for cronie
BuildArch:noarch
%description help
Man pages and other related documents for cronie.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure \
--with-pam \
--with-selinux \
--with-audit \
--with-inotify \
--enable-anacron \
--enable-pie \
--enable-relro

%make_build

%install
%make_install
mkdir -pm700 $RPM_BUILD_ROOT%{_localstatedir}/spool/cron
mkdir -pm755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -pm755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
mkdir -pm755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
mkdir -pm755 $RPM_BUILD_ROOT%{_localstatedir}/spool/anacron

install -m 644 crond.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/crond
install -m 644 contrib/anacrontab $RPM_BUILD_ROOT%{_sysconfdir}/anacrontab
install -m 644 contrib/0hourly $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/0hourly
install -m 755 contrib/0anacron $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/0anacron

touch $RPM_BUILD_ROOT%{_sysconfdir}/cron.deny
touch $RPM_BUILD_ROOT%{_localstatedir}/spool/anacron/{cron.daily,cron.weekly,cron.monthly}

install -m 644 contrib/dailyjobs $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d/dailyjobs

# install systemd initscript
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system/
install -m 644 contrib/cronie.systemd $RPM_BUILD_ROOT/lib/systemd/system/crond.service

%check
make check

%pre

%preun
%systemd_preun crond.service

%post
%systemd_post crond.service
[ -e %{_localstatedir}/spool/anacron/cron.daily ] || touch %{_localstatedir}/spool/anacron/cron.daily 2>/dev/null || :
[ -e %{_localstatedir}/spool/anacron/cron.weekly ] || touch %{_localstatedir}/spool/anacron/cron.weekly 2>/dev/null || :
[ -e %{_localstatedir}/spool/anacron/cron.monthly ] || touch %{_localstatedir}/spool/anacron/cron.monthly 2>/dev/null || :

%postun
%systemd_postun_with_restart crond.service

%triggerin -- pam, glibc, libselinux
systemctl try-restart crond.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root)

%doc AUTHORS ChangeLog COPYING README

%dir %{_sysconfdir}/cron.d
%dir %{_localstatedir}/spool/cron
%dir %{_localstatedir}/spool/anacron
%ghost %attr(0644,root,root) %verify(not md5 size mtime) %{_localstatedir}/spool/anacron/{cron.daily,cron.weekly,cron.monthly}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/cron.d/dailyjobs
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/0anacron
%config(noreplace) %{_sysconfdir}/anacrontab
%config(noreplace) %{_sysconfdir}/pam.d/crond
%config(noreplace) %{_sysconfdir}/cron.deny
%config(noreplace) %{_sysconfdir}/cron.d/0hourly
%attr(0644,root,root) /lib/systemd/system/crond.service
%config(noreplace) %{_sysconfdir}/sysconfig/crond

%{_sbindir}/crond
%{_sbindir}/anacron
%attr(4755,root,root) %{_bindir}/crontab
%{_bindir}/cronnext


%files help
%{_mandir}/{man1,man5,man8}/*


%changelog
* Fri Jul 22 2022 YukariChiba <i@0x7f.cc> - 1.6.1-1
- Upgrade version to 1.6.1

* Thu Dec 30 2021 wangjie <wangjie375@huawei.com> - 1.5.7-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: Update cronie to 1.5.7

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 1.5.5-4
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Fri May 28 2021 panxiaohe <panxiaohe@huawei.com> - 1.5.5-3
- Add automake BuildRequires to use the aclocal program

* Tue Sep 8 2020 wangchen <wangchen137@huawei.com> - 1.5.5-2
- modify the URL of Source0

* Thu Jul 23 2020 Liquor <lirui130@huawei.com> - 1.5.5-1
- update to 1.5.5

* Sat Mar 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.5.4-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix permission of crontab

* Fri Dec 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.5.4-4
- Add requires

* Fri Sep 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.5.4-3
- Add license "ISC"

* Thu Aug 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.5.4-2
- Build noarch for Help Package

* Tue Aug 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.5.4-1
- Package init
