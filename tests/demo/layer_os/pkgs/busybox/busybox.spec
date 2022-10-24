#spec file for busybox
%if "%{!?VERSION:1}"
%define VERSION 1.34.1
%endif

%if "%{!?RELEASE:1}"
%define RELEASE 17
%endif
Epoch: 1

Name: busybox
Version: %{VERSION}
Release: %{RELEASE}
Summary: The Swiss Army Knife of Embedded Linux
License: GPLv2
URL: http://www.busybox.net

Source: http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1: busybox-static.config
Source2: busybox-petitboot.config
Source3: busybox-dynamic.config

Patch6000: backport-CVE-2022-28391.patch
Patch6001: backport-CVE-2022-30065.patch

BuildRoot:      %_topdir/BUILDROOT
#Dependency
BuildRequires: gcc glibc-static
BuildRequires: libselinux-devel >= 1.27.7-2
BuildRequires: libsepol-devel libselinux-static libsepol-static

Provides: bundled(md5-drepper2)

%package petitboot
Summary: Configure the busybox version with petitboot

%package help
Summary: Documentation for busybox

%description
BusyBox combines tiny versions of many common UNIX utilities into a
single small executable. It provides replacements for most of the
utilities you usually find in GNU fileutils, shellutils, etc. It provides
a fairly complete environment for any small or embedded system.

%description petitboot
The Petitboot bootloader provides a boot menu and boots the chosen boot
option using the Linux kernel's kexec functionality. And for use with the
Petitboot bootloader used on PlayStation 3, the version of the contained
in this package is minimal configured.

%description help
This package contains help documentation for busybox

%prep
# auto apply all needed patch with git
%autosetup -n %{name}-%{version} -p1 -v

%build
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

%install
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 755 busybox.petitboot $RPM_BUILD_ROOT/sbin/busybox.petitboot
install -m 755 busybox.dynamic $RPM_BUILD_ROOT/sbin/busybox
install -m 644 docs/busybox.petitboot.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.petitboot.1
install -m 644 docs/busybox.dynamic.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.1

%files
%doc LICENSE README
/sbin/busybox

%files petitboot
%doc LICENSE README
/sbin/busybox.petitboot

%files help
%{_mandir}/man1/busybox.1.gz
%{_mandir}/man1/busybox.petitboot.1.gz

%changelog
* Fri Aug 19 2022 jikui <jikui2@huawei.com> - 1:1.34.1-17
- Type:CVE
- Id:NA
- SUG:NA
- DESC:fix CVE-2022-30065

* Thu Jul 28 2022 jikui <jikui2@huawei.com> - 1:1.34.1-16
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:sync openEuler-22.03-LTS

* Thu May 5 2022 jikui <jikui2@huawei.com> - 1:1.34.1-15
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add epoch field in spec file

* Tue Apr 19 2022 jikui <jikui2@huawei.com> - 1:1.34.1-14
- Type:CVE
- Id:NA
- SUG:NA
- DESC:fix CVE-2022-28391

* Mon Nov 29 2021 jikui <jikui2@huawei.com> - 1:1.34.1-13
- Type:enhancement
- Id:NA
- SUG:NA
- DESC:update busybox to 1.34.1

* Wed Nov 25 2021 xiechengliang <xiechengliang1@huawei.com> - 1:1.33.1-12
- Type:CVE
- Id:NA
- SUG:NA
- DESC:fix CVE-2021-42378 CVE-2021-42379 CVE-2021-42380 CVE-2021-42381 CVE-2021-42382 CVE-2021-42383 CVE-2021-42384 CVE-2021-42385 and CVE-2021-42386

* Wed Nov 24 2021 xiechengliang <xiechengliang1@huawei.com> - 1:1.33.1-11
- Type:CVE
- Id:NA
- SUG:NA
- DESC:fix CVE-2021-42373 CVE-2021-42375 and CVE-2021-42376

* Mon Nov 22 2021 jikui <jikui2@huawei.com> - 1:1.33.1-10
- Type:CVE
- Id:NA
- SUG:NA
- DESC:fix CVE-2021-42374 and CVE-2021-42377

* Fri Aug 13 2021 jikui <jikui2@huawei.com> - 1:1.33.1-9
- Type:enhancement
- Id:NA
- SUG:NA
- DESC:update busybox to 1.33.1

* Fri Apr 30 2021 caihaomin <caihaomin@huawei.com> - 1:1.31.1-8
- Type:CVE
- CVE:CVE-2021-28831
- SUG:NA
- DESC:fix CVE-2021-28831

* Tue Feb 09 2021 xieliuhua <xieliuhua@huawei.com> - 1:1.31.1-7
- Type:CVE
- CVE:CVE-2018-1000500
- SUG:NA
- DESC:fix CVE-2018-1000500

* Wed Jan 8 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:1.31.1-6
- Type:enhancement
- Id:NA
- SUG:NA
- DESC:update busybox to 1.31.1

* Wed May 08 2019 gulining<gulining1@huawei.com> - 1:1.28.3-2.h3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:revert patch for rtos

* Wed Jan 23 2019 gulining<gulining1@huawei.com> - 1:1.28.3-2.h1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix rtos security boot init
	fix svr monit
	fix busybox ash syslog
	fix add fdisk option
	fix memleak
	fix dmesg pretty
	fix crontab remove bug
	fix crond zombie no exit cmd bug
	fix ash rtos history syslog forbit logging passwd
	fix add env RTOS SECURITY PASSWD to control forbit logging passwd
	fix fix getopt segmentation fault
	fix when mount failed clean it creates dev loopN
	fix hostname remove para file support
	fix avoid rsyslog restart twice
	fix get header tar
	fix introduce ftpget timeout when file nogrow
	fix makefile libbb race

