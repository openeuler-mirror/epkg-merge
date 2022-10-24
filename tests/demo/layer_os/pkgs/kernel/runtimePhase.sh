#!/usr/bash

post:kernel%{?package64kb}-devel() {
if [ -f /etc/sysconfig/kernel ]
then
. /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]
then
(cd /usr/src/kernels/%{KernelVer} &&
/usr/bin/find . -type f | while read f; do
hardlink -c /usr/src/kernels/*.oe*.*/$f $f
done)
fi
}

post:kernel%{?package64kb}-tools() {
/sbin/ldconfig
%systemd_post cpupower.service
}

preun:kernel%{?package64kb}-tools() {
%systemd_preun cpupower.service
}

postun:kernel%{?package64kb}-tools() {
/sbin/ldconfig
%systemd_postun cpupower.service
}

post() {
%{_sbindir}/new-kernel-pkg --package kernel --install %{KernelVer} || exit $?

}

preun() {
if [ `uname -i` == "aarch64" ] &&
[ -f /boot/EFI/grub2/grub.cfg ]; then
/usr/bin/sh  %{_sbindir}/mkgrub-menu-%{devel_release}.sh %{version}-%{devel_release}.aarch64  /boot/EFI/grub2/grub.cfg  remove
fi

}

postun() {
%{_sbindir}/new-kernel-pkg --rminitrd --rmmoddep --remove %{KernelVer} || exit $?
if [ -x %{_sbindir}/weak-modules ]
then
%{_sbindir}/weak-modules --remove-kernel %{KernelVer} || exit $?
fi

if [ -d /lib/modules/%{KernelVer} ] && [ "`ls -A  /lib/modules/%{KernelVer}`" = "" ]; then
rm -rf /lib/modules/%{KernelVer}
fi

}

posttrans() {
%{_sbindir}/new-kernel-pkg --package kernel --mkinitrd --dracut --depmod --update %{KernelVer} || exit $?
%{_sbindir}/new-kernel-pkg --package kernel --rpmposttrans %{KernelVer} || exit $?
if [ `uname -i` == "aarch64" ] &&
[ -f /boot/EFI/grub2/grub.cfg ]; then
/usr/bin/sh %{_sbindir}/mkgrub-menu-%{devel_release}.sh %{version}-%{devel_release}.aarch64  /boot/EFI/grub2/grub.cfg  update
fi
if [ -x %{_sbindir}/weak-modules ]
then
%{_sbindir}/weak-modules --add-kernel %{KernelVer} || exit $?
fi
%{_sbindir}/new-kernel-pkg --package kernel --mkinitrd --dracut --depmod --update %{KernelVer} || exit $?
%{_sbindir}/new-kernel-pkg --package kernel --rpmposttrans %{KernelVer} || exit $?

}

