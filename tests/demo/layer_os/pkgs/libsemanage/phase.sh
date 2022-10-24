#!/usr/bash

prep() {
%autosetup -n libsemanage-%{version} -p1

}

build() {
export LDFLAGS="%{?__global_ldflags}"

make clean
%make_build CFLAGS="%{optflags}" swigify
%make_build CFLAGS="%{optflags}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" all
%make_build %{__python3} LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" pywrap

}

install() {
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sharedstatedir}/selinux
mkdir -p %{buildroot}%{_sharedstatedir}/selinux/tmp

make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" install
make PYTHON=%{__python3} DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" install-pywrap

cp %{SOURCE1} %{buildroot}/etc/selinux/semanage.conf
ln -sf  %{_libdir}/libsemanage.so.2 %{buildroot}/%{_libdir}/libsemanage.so

%ldconfig_scriptlets

}

check() {
make test

}

