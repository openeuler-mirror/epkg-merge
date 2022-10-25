#!/usr/bash

post:elfutils-libs() {
-p /sbin/ldconfig
}

postun:elfutils-libs() {
-p /sbin/ldconfig
}

post:elfutils-libelf() {
-p /sbin/ldconfig
}

postun:elfutils-libelf() {
-p /sbin/ldconfig
}

post:elfutils-default-yama-scope() {
if [ -x /usr/lib/systemd/systemd-sysctl ] ; then
%sysctl_apply 10-default-yama-scope.conf
fi
}

post:elfutils-debuginfod-client() {
-p /sbin/ldconfig
}

postun:elfutils-debuginfod-client() {
-p /sbin/ldconfig
}

pre:elfutils-debuginfod() {
getent group debuginfod >/dev/null || groupadd -r debuginfod
getent passwd debuginfod >/dev/null || \
  useradd -r -g debuginfod -d /var/cache/debuginfod -s /sbin/nologin \
          -c "elfutils debuginfo server" debuginfod
exit 0
}

post:elfutils-debuginfod() {
%systemd_post debuginfod.service
}

postun:elfutils-debuginfod() {
%systemd_postun_with_restart debuginfod.service
}

