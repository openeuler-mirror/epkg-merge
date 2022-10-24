#!/usr/bash

pre() {
if [ ! -d %{_localstatedir}/lib/logrotate/ -a -f %{_localstatedir}/lib/logrotate.status ]; then
mkdir -p %{_localstatedir}/lib/logrotate
cp -a %{_localstatedir}/lib/logrotate.status %{_localstatedir}/lib/logrotate
fi

}

preun() {

}

post() {

}

postun() {

}

