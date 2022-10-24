#!/usr/bash

prep() {
%autosetup -n libevent-%{version}-stable -p1

}

build() {
%configure %%{env.configureFlags}
%make_build

}

install() {
%make_install
rm -f %{buildroot}%{_libdir}/*.la

}

check() {
%make_build check

%ldconfig_scriptlets

}

