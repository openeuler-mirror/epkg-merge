#!/usr/bash

prep() {
%setup -q -n %{name}-%{version} -a 1 -c

}

install() {
mkdir -p %{buildroot}%{_lib_path}/brcm
mkdir -p %{buildroot}%{_license_path}
mkdir -p %{buildroot}/boot
cd %{name}-%{version}
install -p -m 644 License/* %{buildroot}%{_license_path}
install -p -m 644 $(find ./ -maxdepth 1 -type f) %{buildroot}%{_lib_path}
install -p -m 644 brcm/* %{buildroot}%{_lib_path}/brcm
cd ../firmware-%{firmware_release}
install -p -m 644 boot/*.bin %{buildroot}/boot
install -p -m 644 boot/*.linux %{buildroot}/boot
install -p -m 644 boot/*.dat %{buildroot}/boot
install -p -m 644 boot/*.elf %{buildroot}/boot
install -p -m 644 boot/LICENCE.* %{buildroot}/boot

cd -

}

