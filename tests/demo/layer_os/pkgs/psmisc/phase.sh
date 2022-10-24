#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure --prefix=%{_prefix} %%{env.configureFlags}
%make_build

}

install() {
%make_install
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/fuser $RPM_BUILD_ROOT%{_sbindir}
%find_lang %name --all-name --with-man

}

