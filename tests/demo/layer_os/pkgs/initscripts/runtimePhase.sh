#!/usr/bash

post:network-scripts() {
chkconfig --add network > /dev/null 2>&1 || :

[ -L %{_sbindir}/ifup ]   || rm -f %{_sbindir}/ifup
[ -L %{_sbindir}/ifdown ] || rm -f %{_sbindir}/ifdown

%{_sbindir}/update-alternatives --install %{_sbindir}/ifup   ifup   %{_sysconfdir}/sysconfig/network-scripts/ifup 90 \
                                --slave   %{_sbindir}/ifdown ifdown %{_sysconfdir}/sysconfig/network-scripts/ifdown \
                                --initscript network
}

preun:network-scripts() {
if [ $1 -eq 0 ]; then
chkconfig --del network > /dev/null 2>&1 || :
%{_sbindir}/update-alternatives --remove ifup %{_sysconfdir}/sysconfig/network-scripts/ifup
fi
}

post:netconsole-service() {
%systemd_post netconsole.service
}

preun:netconsole-service() {
%systemd_preun netconsole.service
}

postun:netconsole-service() {
%systemd_postun netconsole.service
}

post:readonly-root() {
%systemd_post readonly-root.service
}

preun:readonly-root() {
%systemd_preun readonly-root.service
}

postun:readonly-root() {
%systemd_postun readonly-root.service
}

post() {
%systemd_post import-state.service loadmodules.service

}

preun() {
%systemd_preun import-state.service loadmodules.service

}

postun() {
%systemd_postun import-state.service loadmodules.service


}

