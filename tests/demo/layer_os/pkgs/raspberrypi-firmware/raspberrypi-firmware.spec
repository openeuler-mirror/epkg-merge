%global _lib_path /usr/lib/firmware
%global _license_path /usr/share/licenses/raspi
%global firmware_release 1.20220308
%global debug_package %{nil}

Name:		raspberrypi-firmware
Version:	20220316
Release:	6
Summary:	Firmware files used for RaspberryPi
License:	GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
ExclusiveArch: aarch64

Provides:	raspberrypi-firmware = %{version}-%{release}

URL:		https://github.com/raspberrypi/firmware
Source0:	https://github.com/raspberrypi/firmware/archive/%{firmware_release}/firmware-%{firmware_release}.tar.gz
Source1:	%{name}-%{version}.tar.gz
Conflicts:	linux-firmware

%description
This package contains firmware images required by some RaspberryPi devices.

%prep
%setup -q -n %{name}-%{version} -a 1 -c

%install
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

%files
%dir %{_lib_path}
%dir %{_license_path}
%{_lib_path}/*
/boot/*
%license %{_license_path}

%changelog
* Wed Mar 16 2022 Yafen Fang<yafen@iscas.ac.cn> - 20220316-6
- update firmware to version 1.20220308
- update firmware-nonfree to last commit (54ffdd6e2ea6055d46656b78e148fe7def3ec9d8): 1:20190114-2+rpt4 release

* Tue Feb 23 2021 Yafen Fang<yafen@iscas.ac.cn> - 20210223-5
- update firmware files: firmware(1.20210201), bluez-firmware(1.2-4+rpt8: e7fd166981ab4bb9a36c2d1500205a078a35714d) and firmware-nonfree(1:20190114-1+rpt11: 83938f78ca2d5a0ffe0c223bb96d72ccc7b71ca5).

* Tue Nov 10 2020 Yafen Fang<yafen@iscas.ac.cn> - 20201110-4
- update firmware files: firmware(1.20201022), bluez-firmware(a4e08822e3f24a6211f6ac94bc98b7ef87700c70) and firmware-nonfree(5113681d6dcd46581a1882cbeb3d5cf1ddbf7676).

* Tue Sep 22 2020 Yafen Fang<yafen@iscas.ac.cn> - 20200904-3
- Add the conflicts field, declaring the conflicts with linux-firmware(brcmfmac43362-sdio.lemaker,bananapro.txt/brcmfmac43430-sdio.bin/brcmfmac43455-sdio.bin in /usr/lib/firmware/brcm).

* Wed Sep 16 2020 Yafen Fang<yafen@iscas.ac.cn> - 20200904-2
- Change source0's name.

* Fri Sep 4  2020 Yafen Fang<yafen@iscas.ac.cn> - 20200904-1
- Update firmware files.

* Mon 31 Aug 2020 Yafen Fang<yafen@iscas.ac.cn> - 20200717-3
- Add source url in spec.

* Fri Jul 17 2020 Yafen Fang<yafen@iscas.ac.cn> - 20200717-1
- Update firmware files, add licenses.

* Wed May 20 2020 Jianmin Wang<jianmin@iscas.ac.cn> - 20200512-1
- Add firmware file from RaspberryPi firmware, bluez-firmware and firmware-nonfree.
