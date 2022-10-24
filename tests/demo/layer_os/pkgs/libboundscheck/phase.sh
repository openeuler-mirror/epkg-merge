#!/usr/bash

prep() {
%setup -q

}

build() {
make %{?_smp_mflags}

}

install() {
mkdir -p %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_includedir}/
cp lib/*.so %{buildroot}%{_libdir}/
cp include/securec.h %{buildroot}%{_includedir}/
cp include/securectype.h %{buildroot}%{_includedir}/

}

clean() {
rm -rf %{buildroot}

}

