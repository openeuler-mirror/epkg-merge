#!/usr/bash

prep() {
%autosetup -p1

}

build() {
%configure --libdir=/%{_lib} %%{env.configureFlags}
make CFLAGS="%{optflags}" %{?_smp_mflags}

}

install() {
%make_install

rm -f $RPM_BUILD_ROOT/%{_lib}/%{name}.so
rm -f $RPM_BUILD_ROOT/%{_lib}/libdrop_ambient.so
mkdir -p $RPM_BUILD_ROOT%{_libdir}
VLIBNAME=$(ls $RPM_BUILD_ROOT/%{_lib}/%{name}.so.*.*.*)
LIBNAME=$(basename $VLIBNAME)
ln -s ../../%{_lib}/$LIBNAME $RPM_BUILD_ROOT%{_libdir}/%{name}.so
ln -s ../../%{_lib}/libdrop_ambient.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/libdrop_ambient.so
mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libcap-ng.a $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libdrop_ambient.a $RPM_BUILD_ROOT%{_libdir}

%delete_la

}

check() {
make check

%ldconfig_scriptlets

}

