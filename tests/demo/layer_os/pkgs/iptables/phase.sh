#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
./autogen.sh
%configure %%{env.configureFlags}

%disable_rpath

rm -f include/linux/types.h

%make_build

}

install() {
%make_install

%delete_la

install -m 0755 -d %{buildroot}%{_includedir}/iptables
install -m 0644 include/ip*tables.h %{buildroot}%{_includedir}
install -m 0644 include/iptables/internal.h %{buildroot}%{_includedir}/iptables

install -m 0755 -d %{buildroot}%{_includedir}/libipulog/
install -m 0644 include/libipulog/*.h %{buildroot}%{_includedir}/libipulog

install -m 0755 -d %{buildroot}/%{script_path}
install -m 0755 -c %{SOURCE1} %{buildroot}/%{script_path}/iptables.init
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE1} > ip6tables.init
install -m 0755 ip6tables.init %{buildroot}/%{script_path}/ip6tables.init
install -m 0755 -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 0600 -c %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/iptables-config
sed -e 's;iptables;ip6tables;g' -e 's;IPTABLES;IP6TABLES;g' < %{SOURCE2} > ip6tables-config
install -m 0600 -c ip6tables-config %{buildroot}%{_sysconfdir}/sysconfig/ip6tables-config
install -m 0600 -c %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/iptables
install -m 0600 -c %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ip6tables

install -m 0755 -d %{buildroot}%{_unitdir}
install -m 0644 -c %{SOURCE3} %{buildroot}%{_unitdir}
sed -e 's;iptables;ip6tables;g' -e 's;IPv4;IPv6;g' -e 's;/usr/libexec/ip6tables;/usr/libexec/iptables;g' < %{SOURCE3} > ip6tables.service
install -m 0644 -c ip6tables.service %{buildroot}%{_unitdir}

install -m 0755 -d %{buildroot}/%{legacy_actions}/iptables
install -m 0755 -d %{buildroot}/%{legacy_actions}/ip6tables

pushd  %{buildroot}/%{legacy_actions}/iptables
cat << EOF > save
exec %{script_path}/iptables.init save
EOF
chmod 0755 save
popd
sed -e 's;iptables.init;ip6tables.init;g' -e 's;IPTABLES;IP6TABLES;g' < %{buildroot}/%{legacy_actions}/iptables/save > ip6tabes.save-legacy
install -m 0755 -c ip6tabes.save-legacy %{buildroot}/%{legacy_actions}/ip6tables/save

pushd %{buildroot}/%{legacy_actions}/iptables
cat << EOF > panic
exec %{script_path}/iptables.init panic
EOF
chmod 0755 panic
popd
sed -e 's;iptables.init;ip6tables.init;g' -e 's;IPTABLES;IP6TABLES;g' < %{buildroot}/%{legacy_actions}/iptables/panic > ip6tabes.panic-legacy
install -m 0755 -c ip6tabes.panic-legacy %{buildroot}/%{legacy_actions}/ip6tables/panic

install -m 0755 iptables/iptables-apply %{buildroot}%{_sbindir}
install -m 0755 iptables/iptables-apply.8 %{buildroot}%{_mandir}/man8

rm -f %{buildroot}%{_sysconfdir}/ethertypes

touch %{buildroot}%{_libexecdir}/arptables-helper

touch %{buildroot}%{_mandir}/man8/arptables.8
touch %{buildroot}%{_mandir}/man8/arptables-save.8
touch %{buildroot}%{_mandir}/man8/arptables-restore.8
touch %{buildroot}%{_mandir}/man8/ebtables.8

%ldconfig_scriptlets

}

