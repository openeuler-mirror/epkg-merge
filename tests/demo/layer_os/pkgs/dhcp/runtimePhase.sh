#!/usr/bash

pre() {
%global gid_uid 177
if ! getent group dhcpd > /dev/null ; then
groupadd --force --gid %{gid_uid} --system dhcpd
fi

if ! getent passwd dhcpd >/dev/null ; then
if ! getent passwd %{gid_uid} >/dev/null ; then
useradd --system --uid %{gid_uid} --gid dhcpd --home / --shell /sbin/nologin --comment "DHCP server" dhcpd
else
useradd --system --gid dhcpd --home / --shell /sbin/nologin --comment "DHCP server" dhcpd
fi
fi



exit 0

}

preun() {
%systemd_preun dhcpd.service dhcpd6.service dhcrelay.service


}

post() {
/sbin/ldconfig
%systemd_post dhcpd.service dhcpd6.service dhcrelay.service

for servicename in dhcpd dhcpd6 dhcrelay; do
etcservicefile=%{_sysconfdir}/systemd/system/${servicename}.service
if [ -f ${etcservicefile} ]; then
grep -q Type= ${etcservicefile} || sed -i '/\[Service\]/a Type=notify' ${etcservicefile}
sed -i 's/After=network.target/Wants=network-online.target\nAfter=network-online.target/' ${etcservicefile}
fi
done
exit 0

}

postun() {
/sbin/ldconfig
%systemd_postun_with_restart dhcpd.service dhcpd6.service dhcrelay.service

}

