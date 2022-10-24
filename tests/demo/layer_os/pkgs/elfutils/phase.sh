#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure --program-prefix=%{_programprefix}
%make_build

}

install() {
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

%make_install
chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*

rm ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/debuginfod.sh
rm ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/debuginfod.csh

install -Dm0644 config/10-default-yama-scope.conf ${RPM_BUILD_ROOT}%{_sysctldir}/10-default-yama-scope.conf
install -Dm0644 config/debuginfod.service ${RPM_BUILD_ROOT}%{_unitdir}/debuginfod.service
install -Dm0644 config/debuginfod.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/debuginfod
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/cache/debuginfod
touch ${RPM_BUILD_ROOT}%{_localstatedir}/cache/debuginfod/debuginfod.sqlite

}

check() {
%make_build check || (cat tests/test-suite.log; true)

}

clean() {
rm -rf ${RPM_BUILD_ROOT}

}

