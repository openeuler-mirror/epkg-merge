#!/usr/bash

pre() {

}

preun() {
%systemd_preun crond.service

}

post() {
%systemd_post crond.service
[ -e %{_localstatedir}/spool/anacron/cron.daily ] || touch %{_localstatedir}/spool/anacron/cron.daily 2>/dev/null || :
[ -e %{_localstatedir}/spool/anacron/cron.weekly ] || touch %{_localstatedir}/spool/anacron/cron.weekly 2>/dev/null || :
[ -e %{_localstatedir}/spool/anacron/cron.monthly ] || touch %{_localstatedir}/spool/anacron/cron.monthly 2>/dev/null || :

}

postun() {
%systemd_postun_with_restart crond.service

%triggerin -- pam, glibc, libselinux
systemctl try-restart crond.service >/dev/null 2>&1 || :

}

