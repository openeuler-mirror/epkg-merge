#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure
%make_build

}

install() {
%make_install
rm -f %{buildroot}/%{_libdir}/libpopt.la
mkdir -p %{buildroot}/%{_sysconfdir}/popt.d

%find_lang %{name}

}

check() {
make check

}

