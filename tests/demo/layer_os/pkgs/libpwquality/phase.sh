#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure %%{env.configureFlags}

%make_build

}

install() {
export SETUPTOOLS_USE_DISTUTILS=stdlib
%make_install

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_moduledir}/*.la

mkdir %{buildroot}%{_secconfdir}/pwquality.conf.d

%find_lang libpwquality

}

check() {

%ldconfig_scriptlets

}

