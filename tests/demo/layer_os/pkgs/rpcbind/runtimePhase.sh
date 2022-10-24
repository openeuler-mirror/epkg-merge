#!/usr/bash

pre() {
getent group rpc >/dev/null || groupadd -f -g 32 -r rpc
if ! getent passwd rpc >/dev/null ; then
if ! getent passwd 32 >/dev/null ; then
useradd -l -c "Rpcbind Daemon" -d /var/lib/%{name}  \
	      -g rpc -M -s /sbin/nologin -o -u 32 rpc > /dev/null 2>&1
else
useradd -l -c "Rpcbind Daemon" -d /var/lib/%{name}  \
	      -g rpc -M -s /sbin/nologin rpc > /dev/null 2>&1
fi
fi

}

post() {
%systemd_post %{name}.service %{name}.socket

}

preun() {
%systemd_preun %{name}.service %{name}.socket

}

postun() {
%systemd_postun_with_restart %{name}.service %{name}.socket

%triggerun -- %{name} < 0.2.0-15
%{_bindir}/systemd-sysv-convert --save %{name} >/dev/null 2>&1 ||:
/bin/systemctl --no-reload enable %{name}.service >/dev/null 2>&1
/sbin/chkconfig --del %{name} >/dev/null 2>&1 || :
/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :

%triggerin -- %{name} > 0.2.2-2.0
if systemctl -q is-enabled %{name}.socket
then
/bin/systemctl reenable %{name}.socket  >/dev/null 2>&1 || :
/bin/systemctl restart %{name}.socket >/dev/null 2>&1 || :
fi

}

