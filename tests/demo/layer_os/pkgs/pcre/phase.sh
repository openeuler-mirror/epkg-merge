#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
libtoolize -cf
autoreconf -vif
%configure \
%ifarch riscv64
--disable-jit \
%else
--enable-jit \
%endif
%%{env.configureFlags}
%make_build

}

install() {
%make_install
rm -f %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_docdir}/pcre

}

check() {
make check VERBOSE=yes

%ldconfig_scriptlets

}

