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
rm -f %{buildroot}%{python3_sitearch}/kmod/*.la
pushd $RPM_BUILD_ROOT/%{_mandir}/man5
ln -s modprobe.d.5.gz modprobe.conf.5.gz
popd

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
for i in $RPM_BUILD_ROOT%{_sbindir}/modprobe $RPM_BUILD_ROOT%{_sbindir}/modinfo $RPM_BUILD_ROOT%{_sbindir}/insmod \
         $RPM_BUILD_ROOT%{_sbindir}/rmmod $RPM_BUILD_ROOT%{_sbindir}/depmod $RPM_BUILD_ROOT%{_sbindir}/lsmod
do
ln -sf ../bin/kmod $i
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d
mkdir -p $RPM_BUILD_ROOT/sbin

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/weak-modules
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d/dist.conf

}

