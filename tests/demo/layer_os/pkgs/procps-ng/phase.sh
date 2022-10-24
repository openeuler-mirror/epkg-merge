#!/usr/bash

prep() {
%autosetup -n procps-%{version} -p1

cp -p %{SOURCE1} .
cp -p %{SOURCE2} top/

}

build() {
autoreconf -ivf

%configure  --exec-prefix=/ --docdir=/unwanted %%{env.configureFlags}

make CFLAGS="%{optflags}"

}

install() {
%make_install

%find_lang %{name} --all-name --with-man

ln -s %{_bindir}/pidof %{buildroot}%{_sbindir}/pidof

%ldconfig_scriptlets

}

