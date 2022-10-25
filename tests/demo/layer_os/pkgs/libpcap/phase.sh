#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure
%make_build

}

install() {
%make_install

%delete_la_and_a

%ldconfig_scriptlets

}

