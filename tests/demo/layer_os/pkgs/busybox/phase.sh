#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1 -v

}

build() {
export CFLAGS="$RPM_OPT_FLAGS -fPIE" LDFLAGS="-Wl,-z,now"

cp %{SOURCE3} .config
yes "" | make oldconfig && \
cat .config && \
make V=1 %{?_smp_mflags} CC="gcc $RPM_OPT_FLAGS"

cp busybox_unstripped busybox.dynamic
cp docs/busybox.1 docs/busybox.dynamic.1

make clean
cp %{SOURCE2} .config
yes "" | make oldconfig
cat .config && \
make V=1 %{?_smp_mflags} CC="%__cc $RPM_OPT_FLAGS"

cp busybox_unstripped busybox.petitboot
cp docs/busybox.1 docs/busybox.petitboot.1

}

install() {
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 755 busybox.petitboot $RPM_BUILD_ROOT/sbin/busybox.petitboot
install -m 755 busybox.dynamic $RPM_BUILD_ROOT/sbin/busybox
install -m 644 docs/busybox.petitboot.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.petitboot.1
install -m 644 docs/busybox.dynamic.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.1

}

