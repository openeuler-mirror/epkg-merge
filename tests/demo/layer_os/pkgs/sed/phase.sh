#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure %%{env.configureFlags}
make %{?_smp_mflags}

}

install() {
%make_install
%find_lang %{name}

}

