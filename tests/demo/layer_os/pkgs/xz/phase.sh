#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

}

install() {
%make_install

%global profiledir %{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE1} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE2} %{buildroot}%{profiledir}

%find_lang %name

}

check() {
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

}

