#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure %%{env.configureFlags}

%make_build

}

install() {
%make_install
rm -f %{buildroot}/%{_libdir}/*.{a,la}

}

