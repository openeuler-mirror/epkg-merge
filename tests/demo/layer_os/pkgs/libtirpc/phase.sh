#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
sh autogen.sh
autoreconf -fisv
%configure
%make_build

}

install() {
%make_install libdir=/%{_lib} pkgconfigdir=%{_libdir}/pkgconfig
%delete_la

mv %{buildroot}%{_mandir}/man3 %{buildroot}%{_mandir}/man3t

%ldconfig_scriptlets

}

