#!/usr/bash

prep() {
%setup -q -a 0
%patch0   -p1 -b .install-to-destdir-slash-usr
%patch1   -p1 -b .arm64-ilp32
%ifarch aarch64 aarch64_ilp32 x86_64
%patch2   -p1 -b .makefile-cflags
%endif
%patch3   -p1 -b .fix-x32
%patch4   -p1 -b .makefile-add-D_FORTIFY_SOURCE-flag
%patch5   -p1 -b .fix-compile-error

mv %{name}-%{version} setup-%{name}-%{version}

}

build() {
make -C setup-%{name}-%{version} soname='libaio.so.1.0.0' libname='libaio.so.1.0.0'
make

}

install() {
pushd setup-%{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 \
  $RPM_BUILD_ROOT/%{_libdir}/libaio.so.1.0.0
popd
make destdir=$RPM_BUILD_ROOT prefix=/ libdir=/%{_lib} usrlibdir=%{_libdir} \
        includedir=%{_includedir} install

rm -rf %{buildroot}%{_usr}/%{_lib}/libaio.a

%ldconfig_scriptlets

}

check() {
make check

}

