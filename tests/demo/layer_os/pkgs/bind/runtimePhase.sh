#!/usr/bash

post:bind-pkcs11() {
%systemd_post named-pkcs11.service
}

preun:bind-pkcs11() {
%systemd_preun named-pkcs11.service
}

postun:bind-pkcs11() {
%systemd_postun_with_restart named-pkcs11.service
}

post:bind-chroot() {
%systemd_post named-chroot.service
%chroot_fix_devices %{chroot_prefix}
:;
}

posttrans:bind-chroot() {
if [ -x /usr/sbin/selinuxenabled ] && /usr/sbin/selinuxenabled; then
[ -x /sbin/restorecon ] && /sbin/restorecon %{chroot_prefix}/dev/* > /dev/null 2>&1;
fi;
}

preun:bind-chroot() {
%systemd_preun named-chroot.service named-chroot-setup.service
:;
}

postun:bind-chroot() {
%systemd_postun_with_restart named-chroot.service
}

pre() {
if [ "$1" -eq 1 ]; then
/usr/sbin/groupadd -g %{bind_gid} -f -r named >/dev/null 2>&1 || :;
/usr/sbin/useradd  -u %{bind_uid} -r -N -M -g named -s /sbin/nologin -d /var/named -c Named named >/dev/null 2>&1 || :;
fi;
:;

}

post() {
%?ldconfig
if [ -e "%{_sysconfdir}/selinux/config" ]; then
%selinux_set_booleans -s targeted %{selinuxbooleans}
%selinux_set_booleans -s mls %{selinuxbooleans}
fi
if [ "$1" -eq 1 ]; then
[ -x /sbin/restorecon ] && /sbin/restorecon /etc/rndc.* /etc/named.* >/dev/null 2>&1 ;
[ -e /etc/rndc.key ] && chown root:named /etc/rndc.key
[ -e /etc/rndc.key ] && chmod 0640 /etc/rndc.key
else
if getent passwd named | grep ':/bin/false$' >/dev/null; then
/sbin/usermod -s /sbin/nologin named
fi
if /usr/sbin/named-checkconf -p /etc/named.conf 2>/dev/null | grep -q named.iscdlv.key
then
echo "Replacing obsolete named.iscdlv.key with named.root.key..."
if cp -Rf --preserve=all --remove-destination /etc/named.conf /etc/named.conf.rpmbackup; then
sed -e 's/named\.iscdlv\.key/named.root.key/' \
        /etc/named.conf.rpmbackup > /etc/named.conf || \
      mv /etc/named.conf.rpmbackup /etc/named.conf
fi
fi
fi
%systemd_post named.service
:;

}

preun() {
%systemd_preun named.service

}

postun() {
%?ldconfig
%systemd_postun_with_restart named.service
if [ -e "%{_sysconfdir}/selinux/config" ]; then
%selinux_unset_booleans -s targeted %{selinuxbooleans}
%selinux_unset_booleans -s mls %{selinuxbooleans}
fi

}

