#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
make prefix=%{_prefix} lib=%{_lib} LIBDIR=%{_libdir} SBINDIR=%{_sbindir} \
     INCDIR=%{_includedir} MANDIR=%{_mandir} PKGCONFIGDIR=%{_libdir}/pkgconfig/

}

install() {
make install RAISE_SETFCAP=no DESTDIR=%{buildroot} LIBDIR=%{_libdir} SBINDIR=%{_sbindir} PKGCONFIGDIR=%{_libdir}/pkgconfig/

mkdir -p %{buildroot}/%{_mandir}/man{2,3,8}
mv -f doc/*.3 %{buildroot}/%{_mandir}/man3/
chmod +x %{buildroot}/%{_libdir}/*.so.*

}

check() {
%make_build COPTS="%{optflags}" test

}

