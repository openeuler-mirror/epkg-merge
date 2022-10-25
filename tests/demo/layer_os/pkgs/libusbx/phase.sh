#!/usr/bash

prep() {
%autosetup -n %{source}-%{version} -p1

}

build() {
mkdir -p m4
autoreconf -ivf
%configure %%{env.configureFlags}
%make_build
make docs -C doc

}

check() {
make check

}

install() {
%make_install

%ldconfig_scriptlets

}

