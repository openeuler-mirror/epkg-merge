#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
autoreconf
%configure
%make_build

}

install() {
%make_install
%delete_la

}

check() {
make check

}

