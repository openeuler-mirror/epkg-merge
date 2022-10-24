%global nmconfdir %{_sysconfdir}/NetworkManager
%global dhcpconfdir %{_sysconfdir}/dhcp

Name:      dhcp
Version:   4.4.2
Release:   15
Summary:   Dynamic host configuration protocol software
#Please don't change the epoch on this package
Epoch:     12
License:   ISC
URL:       https://www.isc.org/dhcp/
Source0:   http://ftp.isc.org/isc/dhcp/%{version}/dhcp-%{version}.tar.gz
Source1:  dhclient-script
Source2:  README.dhclient.d
Source3:  11-dhclient
Source5:  56dhclient
Source6:  dhcpd.service
Source7:  dhcpd6.service
Source8:  dhcrelay.service

Patch1: backport-0001-change-bug-url.patch
Patch2: backport-0002-additional-dhclient-options.patch
Patch3: backport-0003-Handle-releasing-interfaces-requested-by-sbin-ifup.patch
Patch4: backport-0004-Support-unicast-BOOTP-for-IBM-pSeries-systems-and-ma.patch
Patch5: backport-0005-Change-default-requested-options.patch
Patch6: backport-0006-Various-man-page-only-fixes.patch
Patch7: backport-0007-Change-paths-to-conform-to-our-standards.patch
Patch8: backport-0008-Make-sure-all-open-file-descriptors-are-closed-on-ex.patch
Patch9: backport-0009-Fix-garbage-in-format-string-error.patch
Patch10: backport-0010-Handle-null-timeout.patch
Patch11: backport-0011-Drop-unnecessary-capabilities.patch
Patch12: backport-0012-RFC-3442-Classless-Static-Route-Option-for-DHCPv4-51.patch
Patch13: backport-0013-DHCPv6-over-PPP-support-626514.patch
Patch14: backport-0014-IPoIB-support-660681.patch
Patch15: backport-0015-Add-GUID-DUID-to-dhcpd-logs-1064416.patch
Patch16: backport-0016-Turn-on-creating-sending-of-DUID.patch
Patch17: backport-0017-Send-unicast-request-release-via-correct-interface.patch
Patch18: backport-0018-No-subnet-declaration-for-iface-should-be-info-not-e.patch
Patch19: backport-0019-dhclient-write-DUID_LLT-even-in-stateless-mode-11563.patch
Patch20: backport-0020-Discover-all-hwaddress-for-xid-uniqueness.patch
Patch21: backport-0021-Load-leases-DB-in-non-replay-mode-only.patch
Patch22: backport-0022-dhclient-make-sure-link-local-address-is-ready-in-st.patch
Patch23: backport-0023-option-97-pxe-client-id.patch
Patch24: backport-0024-Detect-system-time-changes.patch
Patch25: backport-0025-bind-Detect-system-time-changes.patch
Patch26: backport-0026-Add-dhclient-5-B-option-description.patch
Patch27: backport-0027-Add-missed-sd-notify-patch-to-manage-dhcpd-with-syst.patch

Patch28: bugfix-dhcp-4.2.5-check-dhclient-pid.patch
Patch29: bugfix-reduce-getifaddr-calls.patch

Patch30: bugfix-dhcpd-2038-problem.patch
Patch31: dhcpd-coredump-infiniband.patch
Patch32: bugfix-dhclient-check-if-pid-was-held.patch
Patch33: bugfix-dhcp-64-bit-lease-parse.patch
Patch34: backport-CVE-2021-25217.patch
Patch35: fix-multiple-definition-with-gcc-10-1.patch
Patch36: fix-multiple-definition-with-gcc-10-2.patch

Patch37: fix-coredump-when-client-active-is-NULL.patch
Patch38: feature-lease-time-config-ipv6.patch
Patch39: add-a-test-case-to-parse-code93-in-option_unittest.patch
Patch40: bugfix-error-message-display.patch
Patch41: backport-Fix-CVE-2021-25214.patch
Patch42: backport-Fix-CVE-2021-25215.patch
Patch43: backport-Fix-CVE-2021-25219.patch
Patch44: backport-Fix-CVE-2021-25220.patch
Patch45: backport-Fix-CVE-2022-2928.patch
Patch46: backport-Fix-CVE-2022-2929.patch

BuildRequires: gcc autoconf automake libtool openldap-devel krb5-devel libcap-ng-devel
BuildRequires: systemd systemd-devel

Requires: shadow-utils coreutils grep sed systemd gawk ipcalc iproute iputils


Provides:  %{name}-common %{name}-libs %{name}-server %{name}-relay %{name}-compat %{name}-client
Obsoletes: %{name}-common %{name}-libs %{name}-server %{name}-relay %{name}-compat %{name}-client


Provides:  dhcp = %{epoch}:%{version}-%{release}
Obsoletes: dhcp < %{epoch}:%{version}-%{release}

Provides: dhclient = %{epoch}:%{version}-%{release}
Obsoletes: dhclient < %{epoch}:%{version}-%{release}


%description
The Dynamic Host Configuration Protocol (DHCP) is a network management protocol used on UDP/IP networks whereby a DHCP server dynamically assigns an IP address and other network configuration parameters to each device on a network so they can communicate with other IP networks.

%package devel
Summary: Development headers and libraries for interfacing to the DHCP server
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for using the ISC DHCP libraries.  The
libdhcpctl and libomapi static libraries are also included in this package.

%package_help

%prep
%setup -n %{name}-%{version}
pushd bind
tar -xvf bind.tar.gz
ln -s bind-9* bind
popd
%autopatch -p1 
#rm bind/bind.tar.gz

sed -i -e 's|/var/db/|%{_localstatedir}/lib/dhcpd/|g' contrib/dhcp-lease-list.pl

%build
autoreconf --verbose --force --install

CFLAGS="%{optflags} -fno-strict-aliasing" \
%configure --with-srv-lease-file=%{_localstatedir}/lib/dhcpd/dhcpd.leases \
    --with-srv6-lease-file=%{_localstatedir}/lib/dhcpd/dhcpd6.leases \
    --with-cli-lease-file=%{_localstatedir}/lib/dhclient/dhclient.leases \
    --with-cli6-lease-file=%{_localstatedir}/lib/dhclient/dhclient6.leases \
    --with-srv-pid-file=%{_localstatedir}/run/dhcpd.pid \
    --with-srv6-pid-file=%{_localstatedir}/run/dhcpd6.pid \
    --with-cli-pid-file=%{_localstatedir}/run/dhclient.pid \
    --with-cli6-pid-file=%{_localstatedir}/run/dhclient6.pid \
    --with-relay-pid-file=%{_localstatedir}/run/dhcrelay.pid \
    --with-ldap --with-ldapcrypto --with-ldap-gssapi --disable-static  --enable-log-pid --enable-paranoia --enable-early-chroot \
    --enable-binary-leases --with-systemd

make

%install
%make_install

install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/dhclient-script

install -p -m 0644 %{SOURCE2} .

mkdir -p $RPM_BUILD_ROOT%{dhcpconfdir}/dhclient.d

mkdir -p $RPM_BUILD_ROOT%{nmconfdir}/dispatcher.d
install -p -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{nmconfdir}/dispatcher.d

install -D -p -m 0755 %{SOURCE5} $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d/56dhclient

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_unitdir}

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dhcpd/
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/dhcpd/dhcpd.leases
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/dhcpd/dhcpd6.leases
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dhclient/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/dhcpd
# WARNING: This file is NOT used anymore.

# If you are here to restrict what interfaces should dhcpd listen on,
# be aware that dhcpd listens *only* on interfaces for which it finds subnet
# declaration in dhcpd.conf. It means that explicitly enumerating interfaces
# also on command line should not be required in most cases.

# If you still insist on adding some command line options,
# copy dhcpd.service from /lib/systemd/system to /etc/systemd/system and modify
# it there.
# https://fedoraproject.org/wiki/Systemd#How_do_I_customize_a_unit_file.2F_add_a_custom_unit_file.3F

# example:
# $ cp /usr/lib/systemd/system/dhcpd.service /etc/systemd/system/
# $ vi /etc/systemd/system/dhcpd.service
# $ ExecStart=/usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid <your_interface_name(s)>
# $ systemctl --system daemon-reload
# $ systemctl restart dhcpd.service
EOF

mkdir -p $RPM_BUILD_ROOT%{dhcpconfdir}
cat << EOF > %{buildroot}%{dhcpconfdir}/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
EOF
cat << EOF > %{buildroot}%{dhcpconfdir}/dhcpd6.conf
#
# DHCPv6 Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd6.conf.example
#   see dhcpd.conf(5) man page
#
EOF

rm -f $RPM_BUILD_ROOT/usr/lib/debug/usr/sbin/dhcrelay-4.3.6-28.7.aarch64.debug

mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-client
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-server

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/dhclient.conf.example doc/examples/dhclient-dhcpv4.conf
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/dhcpd.conf.example doc/examples/dhcpd-dhcpv4.conf
install -p -m 0755 doc/examples/dhclient-dhcpv4.conf $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-client/dhclient.conf.example
install -p -m 0755 doc/examples/dhcpd-dhcpv4.conf $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-server/dhcpd.conf.example

install -p -m 0755 doc/examples/dhclient-dhcpv6.conf $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-client/dhclient6.conf.example
install -p -m 0755 doc/examples/dhcpd-dhcpv6.conf $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-server/dhcpd6.conf.example
install -p -m 0755 server/dhcpd.conf.example $RPM_BUILD_ROOT%{_datadir}/doc/dhcp-server/dhcpd.conf.example

install -D -p -m 0644 contrib/ldap/dhcp.schema $RPM_BUILD_ROOT%{_sysconfdir}/openldap/schema/dhcp.schema

find $RPM_BUILD_ROOT -type f -name "*.la" -delete -print

%check
make check

%pre
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

%preun
%systemd_preun dhcpd.service dhcpd6.service dhcrelay.service


%post
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

%postun
/sbin/ldconfig
%systemd_postun_with_restart dhcpd.service dhcpd6.service dhcrelay.service

%files
%defattr(-,root,root)
%license LICENSE
%doc README RELNOTES doc/References.txt
%doc README.dhclient.d
%doc contrib/ldap/ contrib/dhcp-lease-list.pl
%{_datadir}/doc/dhcp-client/dhclient.conf.example
%{_datadir}/doc/dhcp-server/dhcpd.conf.example
%{_datadir}/doc/dhcp-client/dhclient6.conf.example
%{_datadir}/doc/dhcp-server/dhcpd6.conf.example
%{_datadir}/doc/dhcp-server/dhcpd.conf.example
%dir %{_sysconfdir}/openldap/schema
%config(noreplace) %{_sysconfdir}/openldap/schema/dhcp.schema
%attr(0750,root,root) %dir %{dhcpconfdir}
%dir %{_localstatedir}/lib/dhclient
%dir %{dhcpconfdir}/dhclient.d
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%{_sysconfdir}/NetworkManager/dispatcher.d/11-dhclient
%attr(0644,root,root)   %{_unitdir}/dhcpd.service
%attr(0644,root,root)   %{_unitdir}/dhcpd6.service
%attr(0644,root,root) %{_unitdir}/dhcrelay.service
%attr(0755,dhcpd,dhcpd) %dir %{_localstatedir}/lib/dhcpd
%attr(0644,dhcpd,dhcpd) %verify(mode) %config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd.leases
%attr(0644,dhcpd,dhcpd) %verify(mode) %config(noreplace) %{_localstatedir}/lib/dhcpd/dhcpd6.leases
%config(noreplace) %{_sysconfdir}/sysconfig/dhcpd
%config(noreplace) %{dhcpconfdir}/dhcpd.conf
%config(noreplace) %{dhcpconfdir}/dhcpd6.conf
%{_sbindir}/dhcpd
%{_sbindir}/dhclient
%{_sbindir}/dhclient-script
%{_sbindir}/dhcrelay
%{_bindir}/omshell
%attr(0755,root,root) %{_libdir}/pm-utils/sleep.d/56dhclient

%files  devel
%defattr(-,root,root)
%doc doc/IANA-arp-parameters doc/api+protocol
%{_includedir}/dhcpctl
%{_includedir}/omapip
%{_libdir}/libdhcp*.a
%{_libdir}/libomapi.a


%files help
%defattr(644,root,root)
%doc doc/*
%{_mandir}/man1/omshell.1.gz
%{_mandir}/man5/dhcpd.conf.5.gz
%{_mandir}/man5/dhcpd.leases.5.gz
%{_mandir}/man8/dhcpd.8.gz
%{_mandir}/man5/dhcp-options.5.gz
%{_mandir}/man5/dhcp-eval.5.gz
%{_mandir}/man5/dhclient.conf.5.gz
%{_mandir}/man5/dhclient.leases.5.gz
%{_mandir}/man8/dhclient.8.gz
%{_mandir}/man8/dhclient-script.8.gz
%{_mandir}/man8/dhcrelay.8.gz
%{_mandir}/man3/dhcpctl.3.gz
%{_mandir}/man3/omapi.3.gz

%changelog
* Mon Oct 17 2022 renmingshuai <renmingshuai@huawei.com> - 12:4.4.2-15
- Type:cves
- ID:CVE-2022-2928,CVE-2022-2929
- SUG:restart
- DESC:Fix CVE-2022-2928 and CVE-2022-2929

* Tue Sep 27 2022 renmingshuai <renmingshuai@huawei.com> - 12:4.4.2-14
- Type:cves
- ID:CVE-2021-25214, CVE-2021-25215, CVE-2021-25219, CVE-2021-25220
- SUG:restart
- DESC:Fix CVE-2021-25214 CVE-2021-25215 CVE-2021-25219 CVE-2021-25220

* Sat Jul 30 2022 renmingshuai <renmingshuai@huawei.com> - 4.4.2-13
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:add dhX.conf.example in doc

* Tue Feb 22 2022 zengwefeng <zwfeng@huawei.com> - 4.4.2-12
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix error message display

* Wed Jan 12 2022 renmingshuai <renmingshuai@huawei.com> - 4.4.2-11
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:rename upstream patches and add reference

* Fri Jan 07 2022 renmingshuai <renmingshuai@huawei.com> - 4.4.2-10
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:remove buildrequires bind-export-devel and buildin bind

* Fri Nov 26 2021 renmingshuai <renmingshuai@huawei.com> - 4.4.2-9
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix coredump when client active is NULL, add lease time config ipv6 and add a unittest

* Tue Sep 14 2021 panchenbo<panchenbo@uniontech.com.com> - 4.4.2-8
- DESC: install dhcpd.conf.example

* Fri Jul 30 2021 renmingshuai <renmingshuai@huawei.com> - 4.4.2-7
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix multiple defination with gcc 10

* Mon May 31 2021 renmingshuai <renmingshuai@huawei.com> - 4.4.2-6
- Type:CVE
- ID:NA
- SUG:restart
- DESC:CVE-2021-25217

* Sat Feb 20 2021 hanzhijun <hanzhijun1@huawei.com> - 4.4.2-5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:dhcp remove buildin bind

* Tue Dec 29 2020 quanhongfei <quanhongfei@huawei.com> - 4.4.2-4
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix dhcp 64_bit lease parse 

* Thu Sep 10 2020 gaihuiying <gaihuiying1@huawei.com> - 4.4.2-3
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: change ownership of /var/lib/dhcpd/ to dhcpd:dhcpd

* Tue Sep 01 2020 yuboyun <yuboyun@huawei.com> - 4.4.2-2
- Type:NA
- ID:NA
- SUG:NA
- DESC: add yaml file

* Wed Jul 22 2020 gaihuiying<gaihuiying1@huawei.com> - 4.4.2-1
- Type:requirement
- ID:NA
- SUG:restart
- DESC: update to 4.4.2

* Tue Mar 3 2020 zhanglu<zhanglu37@huawei.com> - 4.3.6-37
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: recheck if last pid was held by other process

* Thu Feb 27 2020 zhanglu<zhanglu37@huawei.com> - 4.3.6-36
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: check if last pid when held by other process

* Wed Jan 22 2020 zhanglu<zhanglu37@huawei.com> - 4.3.6-35
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: modify dhcpd coredump when discover interfaces

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-34
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: delete patches

* Tue Dec 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-33
- rename doc subpackage as help subpackage

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-32
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix dhcpd 2038 problem;
       Adds address prefix len to dhclient cli

* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-31
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: reducing getifaddrs calls and improving code performance

* Mon Sep 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-30
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:Fix dhcp package installation failed

* Thu Sep 5 2019 hufeng <solar.hu@huawei.com> - 4.3.6-29
-Create dhcp spec
