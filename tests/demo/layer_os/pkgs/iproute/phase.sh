#!/usr/bash

prep() {
%autosetup -n %{name}2-%{version} -p1

}

build() {
export LIBDIR='%{_libdir}'
export IPT_LIB_DIR='/%{_lib}/xtables'
%configure
%make_build

}

install() {
export CONFDIR='%{_sysconfdir}/iproute2'
export SBINDIR='%{_sbindir}'
export LIBDIR='%{_libdir}'
export DOCDIR='%{_docdir}'

%make_install

install -m 0755 -d %{buildroot}%{_includedir}
install -m 0644 include/libnetlink.h %{buildroot}%{_includedir}/libnetlink.h
install -m 0644 lib/libnetlink.a %{buildroot}%{_libdir}/libnetlink.a

}

