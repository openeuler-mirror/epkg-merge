#!/usr/bash

pre() {

}

post() {
for n in /var/log/{messages,secure,maillog,spooler}
do
[ -f $n ] && continue
umask 066 && touch $n
done

%if %{systemd_lived} == 1
%systemd_post rsyslog.service

%endif
}

preun() {
%systemd_preun rsyslog.service

}

postun() {
%systemd_postun_with_restart rsyslog.service

}

