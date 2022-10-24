#!/usr/bash

prep() {
%autosetup -p1 -n %{name}-%{version}

}

build() {
%configure \
%ifarch riscv64
--disable-multi-os-directory \
%endif
%%{env.configureFlags}

%make_build

}

install() {
%make_install
%delete_la

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%ldconfig_scriptlets

}

check() {
%make_build check

}

