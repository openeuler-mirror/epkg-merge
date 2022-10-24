#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p2

}

build() {
make clean
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}"

}

install() {
rm -rf %{buildroot}
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" install

}

