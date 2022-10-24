#!/usr/bash

post() {
pfx=%{_sbindir}/iptables
pfx6=%{_sbindir}/ip6tables
%{_sbindir}/update-alternatives --install \
	$pfx iptables $pfx-legacy 10 \
	--slave $pfx6 ip6tables $pfx6-legacy \
        --slave $pfx-restore iptables-restore $pfx-legacy-restore \
        --slave $pfx-save iptables-save $pfx-legacy-save \
        --slave $pfx6-restore ip6tables-restore $pfx6-legacy-restore \
        --slave $pfx6-save ip6tables-save $pfx6-legacy-save

%systemd_post iptables.service ip6tables.service

}

preun() {
%systemd_preun iptables.service ip6tables.service

}

postun() {
if [ $1 -eq 0 ]; then
%{_sbindir}/update-alternatives --remove \
		iptables %{_sbindir}/iptables-legacy
fi
%?ldconfig
%systemd_postun iptables.service ip6tables.service

}

