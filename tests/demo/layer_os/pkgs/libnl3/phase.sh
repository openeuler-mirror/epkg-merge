#!/usr/bash

prep() {
%autosetup -n libnl-%{version} -p1

}

build() {
autoreconf -vif
%configure %%{env.configureFlags}
%make_build

cd python
CFLAGS="$RPM_OPT_FLAGS" %py3_build
CFLAGS="$RPM_OPT_FLAGS" %py3_build

}

install() {
%make_install

find $RPM_BUILD_ROOT -name *.la |xargs rm -f

cd python
%py3_install

}

check() {
make check

cd python
%{__python3} setup.py check

%ldconfig_scriptlets

}

