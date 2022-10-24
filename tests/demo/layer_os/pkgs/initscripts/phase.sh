#!/usr/bash

prep() {
%autosetup -p1


}

build() {
%make_build


}

install() {
%make_install

%find_lang %{name}

%ifnarch s390 s390x
rm -f %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ctc
%endif

install -m 0755 -d %{buildroot}%{_docdir}/network-scripts

ln -s  %{_docdir}/%{name}/sysconfig.txt %{buildroot}%{_docdir}/network-scripts/
ln -sr %{_mandir}/man8/ifup.8           %{buildroot}%{_mandir}/man8/ifdown.8

touch %{buildroot}%{_sbindir}/ifup
touch %{buildroot}%{_sbindir}/ifdown


}

