#!/usr/bash

prep() {
%autosetup -p1

autoreconf -fiv
}

build() {
%configure CFLAGS="$RPM_OPT_FLAGS -fPIC" DOCBOOK_TO_MAN="xmlto man --skip-validation"
%make_build

}

install() {
%makeinstall
find %{buildroot} -type f -name changelog -delete

}

check() {
make check

%ldconfig_scriptlets

}

