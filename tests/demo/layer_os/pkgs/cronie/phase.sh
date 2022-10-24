#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure %%{env.configureFlags}

%make_build

}

install() {
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

mkdir -p $RPM_BUILD_ROOT/lib/systemd/system/
install -m 644 contrib/cronie.systemd $RPM_BUILD_ROOT/lib/systemd/system/crond.service

}

check() {
make check

}

