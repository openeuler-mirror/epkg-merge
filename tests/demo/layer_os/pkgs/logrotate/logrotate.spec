%global _configure ../configure

Name: logrotate
Version: 3.20.1
Release: 1
Summary: simplify the administration of log files
License: GPLv2+
Url: https://github.com/logrotate/logrotate
Source0: https://github.com/logrotate/logrotate/releases/download/%{version}/logrotate-%{version}.tar.xz
# lockState: do not print `error:` when exit code is unaffected
Patch0: 0001-logrotate-3.20.1-lock-state-msg.patch 
BuildRequires: acl gcc automake libacl-devel libselinux-devel popt-devel
Requires: coreutils

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  Logrotate
allows for the automatic rotation compression, removal and mailing of
log files.logrotate  Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
mkdir build && cd build
%configure --with-state-file-path=%{_localstatedir}/lib/logrotate/logrotate.status
%make_build V=1

%install
%make_install -C build

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
mkdir -p %{buildroot}%{_localstatedir}/lib/logrotate

install -p -m 644 examples/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.conf
install -p -m 644 examples/*tmp %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 755 examples/logrotate.cron %{buildroot}%{_sysconfdir}/cron.daily/logrotate

%check
%make_build -C build check

%pre
# create it and copy the /var/lib/logrotate.status in it.
if [ ! -d %{_localstatedir}/lib/logrotate/ -a -f %{_localstatedir}/lib/logrotate.status ]; then
  mkdir -p %{_localstatedir}/lib/logrotate
  cp -a %{_localstatedir}/lib/logrotate.status %{_localstatedir}/lib/logrotate
fi

%preun

%post

%postun

%files
%defattr(-,root,root)
%license COPYING
%dir %{_sysconfdir}/cron.daily
%config(noreplace) %{_sysconfdir}/cron.daily/logrotate
%config(noreplace) %{_sysconfdir}/logrotate.conf
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/*tmp
%{_sbindir}/logrotate
%dir %{_localstatedir}/lib/logrotate
%ghost %verify(not size md5 mtime) %attr(0644, root, root) %{_localstatedir}/lib/logrotate/logrotate.status

%files help
%defattr(-,root,root)
%doc ChangeLog.md
%{_mandir}/man8/logrotate.8*
%{_mandir}/man5/logrotate.conf.5*

%changelog
* Fri Jun 10 2022 duyiwei <duyiwei@kylinos.cn> - 3.20.1-1
- upgrade version to 3.20.1 and fix CVE-2022-1348

* Sat Nov 20 2021 xiechengliang <xiechengliang1@huawei.com> - 3.18.1-1
- update upstream to 3.18.1

* Wed Jul 29 2020 tianwei <tianwei12@huawei.com> - 3.17.0-1
- update upstream to 3.17.0

* Fri Apr 24 2020 BruceGW <gyl93216@163.com> - 3.16.0-1
- update upstream to 3.16.0

* Tue Jan 14 2020 openEuler Buildteam <buildteam@huawei.com> - 3.15.1-2
- del unuse info

* Sat Oct 12 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.15.1-1
- update version to 3.15.1
