#!/usr/bash

post:e2fsprogs-devel() {
if [ -f %{_infodir}/libext2fs.info.gz ]; then
/sbin/install-info %{_infodir}/libext2fs.info.gz %{_infodir}/dir || :
fi
}

preun:e2fsprogs-devel() {
if [ $1 = 0 -a -f %{_infodir}/libext2fs.info.gz ]; then
/sbin/install-info --delete %{_infodir}/libext2fs.info.gz %{_infodir}/dir || :
fi
exit 0
}

