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

}

check() {
make check

}

