#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
export CPPFLAGS="-I%{_includedir}/ncurses"
%configure %%{env.configureFlags}
%make_build

}

install() {
%make_install

%ldconfig_scriptlets

}

