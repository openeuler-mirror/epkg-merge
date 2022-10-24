#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
make SHARED="no" ZLIB="no" LIBKMOD=yes STRIP="" OPT="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" PREFIX="/usr" %{?_smp_mflags}
mv lib/libpci.a lib/libpci.a.tobak

make clean

make SHARED="yes" ZLIB="no" LIBKMOD=yes STRIP="" OPT="$RPM_OPT_FLAGS"  PREFIX="/usr" LIBDIR="/%{_lib}"  %{?_smp_mflags}
sed -i "s|^libdir=.*$|libdir=/%{_lib}|" lib/libpci.pc

}

install() {
make install PREFIX=$RPM_BUILD_ROOT/usr SBINDIR=$RPM_BUILD_ROOT/sbin \
             ROOT=$RPM_BUILD_ROOT/ MANDIR=$RPM_BUILD_ROOT/%{_mandir} STRIP="" \
             SHARED="yes" LIBDIR=$RPM_BUILD_ROOT/%{_lib}

install -d $RPM_BUILD_ROOT/{%{_libdir}/pkgconfig,%{_includedir}/pci}
mv lib/libpci.a.tobak lib/libpci.a
install -p -m 644 lib/libpci.a $RPM_BUILD_ROOT%{_libdir}
cp -p lib/{pci,header,config,types}.h $RPM_BUILD_ROOT%{_includedir}/pci
install -p lib/config.h $RPM_BUILD_ROOT%{_includedir}/pci/config.%{_lib}.h
/sbin/ldconfig -N $RPM_BUILD_ROOT%{_libdir}
install -p lib/libpci.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -D -m 0644 lib/libpci.pc %{buildroot}%{_libdir}/pkgconfig/libpci.pc
install -p lib/libpci.so.* $RPM_BUILD_ROOT/%{_lib}/
ln -s ../../%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/*.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libpci.so
rm -rf $RPM_BUILD_ROOT/usr/share/hwdata/pci.ids*

}

clean() {
rm -rf $RPM_BUILD_ROOT

}

