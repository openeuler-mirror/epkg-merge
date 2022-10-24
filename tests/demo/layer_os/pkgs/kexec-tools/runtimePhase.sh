#!/usr/bash

post() {
%systemd_post kdump.service

touch /etc/kdump.conf
if [ -d /proc/bus/mckinley ]
then
sed -e's/\(^KDUMP_COMMANDLINE_APPEND.*\)\("$\)/\1 machvec=dig"/' \
	/etc/sysconfig/kdump > /etc/sysconfig/kdump.new
mv /etc/sysconfig/kdump.new /etc/sysconfig/kdump
elif [ -d /proc/sgi_sn ]
then
sed -e's/\(^KEXEC_ARGS.*\)\("$\)/\1 --noio"/' \
	/etc/sysconfig/kdump > /etc/sysconfig/kdump.new
mv /etc/sysconfig/kdump.new /etc/sysconfig/kdump
fi


}

postun() {
%systemd_postun_with_restart kdump.service

}

preun() {
%systemd_preun kdump.service

%triggerun -- kexec-tools < 2.0.2-3
/usr/bin/systemd-sysv-convert --save kdump >/dev/null 2>&1 ||:
/sbin/chkconfig --del kdump >/dev/null 2>&1 || :
/bin/systemctl try-restart kdump.service >/dev/null 2>&1 || :

%triggerin -- kernel-kdump
touch %{_sysconfdir}/kdump.conf

%triggerpostun -- kernel kernel-xen kernel-debug kernel-PAE kernel-kdump
IMGDIR=/boot
for i in `ls $IMGDIR/initramfs*kdump.img 2>/dev/null`
do
KDVER=`echo $i | sed -e's/^.*initramfs-//' -e's/kdump.*$//'`
if [ ! -e $IMGDIR/vmlinuz-$KDVER ]
then
rm -f $i
fi
done


}

