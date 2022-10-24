#!/usr/bash

post() {
/sbin/ldconfig
if [ ! -e /var/log/tallylog ] ; then
/usr/bin/install -m 600 /dev/null /var/log/tallylog || :
fi

}

postun() {
-p /sbin/ldconfig

}

