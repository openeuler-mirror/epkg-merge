#!/usr/bash

post:libffi-help() {
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/libffi.info.gz || :
}

preun:libffi-help() {
if [ $1 = 0 ] ;then
/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/libffi.info.gz || :
fi
}

