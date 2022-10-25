#!/usr/bash

pre() {
if [ "$1" = "2" ]; then
%if 0%{?is_systemd}
systemctl stop lcrd &>/dev/null
systemctl disable lcrd &>/dev/null
if [ -e %{_sysconfdir}/isulad/daemon.json ];then
sed -i 's#/etc/default/lcrd/hooks#/etc/default/isulad/hooks#g' %{_sysconfdir}/isulad/daemon.json
fi
%else
/sbin/chkconfig --del lcrd &>/dev/null
%endif
fi

}

post() {
if ! getent group isula > /dev/null; then
groupadd --system isula
fi

if [ "$1" = "1" ]; then
%if 0%{?is_systemd}
systemctl enable isulad
systemctl start isulad
%else
/sbin/chkconfig --add isulad
%endif
elif [ "$1" = "2" ]; then
%if 0%{?is_systemd}
# support update from lcrd to isulad, will remove in next version
if [ -e %{_unitdir}/lcrd.service.rpmsave ]; then
mv %{_unitdir}/lcrd.service.rpmsave %{_unitdir}/isulad.service
sed -i 's/lcrd/isulad/g' %{_unitdir}/isulad.service
fi
systemctl status isulad | grep 'Active:' | grep 'running'
if [ $? -eq 0 ]; then
systemctl restart isulad
else
systemctl start isulad
fi
%else
/sbin/service isulad status | grep 'Active:' | grep 'running'
if [ $? -eq 0 ]; then
/sbin/service isulad restart
fi
%endif
fi

if ! getent group isula > /dev/null; then
groupadd --system isula
fi

}

preun() {
%if 0%{?is_systemd}
%systemd_preun isulad
%else
if [ $1 -eq 0 ] ; then
/sbin/service isulad stop >/dev/null 2>&1
/sbin/chkconfig --del isulad
fi
%endif

}

postun() {
%if 0%{?is_systemd}
%systemd_postun_with_restart isulad
%else
if [ "$1" -ge "1" ] ; then
/sbin/service isulad condrestart >/dev/null 2>&1 || :
fi
%endif

}

