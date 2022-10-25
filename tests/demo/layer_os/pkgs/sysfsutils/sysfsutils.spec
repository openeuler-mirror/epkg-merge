Name:        sysfsutils
Version:     2.1.1
Release:     1
Summary:     A set of utilities for interfacing with sysfs
License:     GPLv2 and LGPLv2+
URL:         https://github.com/linux-ras/sysfsutils

Source0:     https://github.com/linux-ras/sysfsutils/archive/v%{version}.tar.gz


BuildRequires: gcc chrpath autoconf automake make libtool
Provides:      libsysfs libsysfs%{?_isa}
Obsoletes:     libsysfs


%description
This package's purpose is to provide a set of utilities for interfacing
with sysfs, a virtual filesystem in Linux kernel versions 2.5+ that
provides a tree of system devices.


%package        devel
Summary:        Including header files and library for the developing of sysfsutils
License:        LGPLv2+
Requires:       sysfsutils = %{version}-%{release}
Provides:       libsysfs-devel
Obsoletes:      libsysfs-devel

%description    devel
This contains dynamic libraries and header files for the developing of sysfsutils.

%package        help
Summary:        Including man files for sysfsutils
Requires:       man
BuildArch:      noarch

%description    help
This contains man files for the using of sysfsutils.

%prep
%autosetup -n %{name}-%{version} -p1

%build
./autogen
%configure --disable-static --libdir=/%{_lib}
%make_build

%check
make check

%install
%make_install

rm -f %{buildroot}/%{_bindir}/dlist_test
rm -f %{buildroot}/%{_bindir}/get_device
rm -f %{buildroot}/%{_bindir}/get_driver
rm -f %{buildroot}/%{_lib}/libsysfs.la

chrpath -d  $(find $RPM_BUILD_ROOT -name get_module)
chrpath -d  $(find $RPM_BUILD_ROOT -name systool)

%ldconfig_scriptlets

%files
%license COPYING cmd/GPL lib/LGPL
%doc README
%{_bindir}/systool
/%{_lib}/libsysfs.so.*

%files devel
%dir %{_includedir}/sysfs
%{_includedir}/sysfs/libsysfs.h
%{_includedir}/sysfs/dlist.h
/%{_lib}/libsysfs.so
/%{_lib}/pkgconfig/libsysfs.pc

%files help
%{_mandir}/man1/systool.1.gz



%changelog
* Thu Nov 25 2021 yanglongkang <yanglongkang@huawei.com> - 2.1.1-1
- update to 2.1.1

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 2.1.0-32
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Wed Nov 4 2020 lixiaokeng <lixiaokeng@huawei.com> - 2.1.0-31
- add make check

* Mon Jul 13 2020 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 2.1.0-30
- backport upstream bugfix patches

* Tue Jun 30 2020 volcanodragon <linfeilong@huawei.com> - 2.1.0-29
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:rename patches

* Fri Jan 10 2020 Huangzheng <huangzheng22@huawei.com> - 2.1.0-28
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:repackaged

* Tue Aug 20 2019 zhanghaibo <ted.zhang@huawei.com> - 2.1.0-27
- Type:enhancemnet
- ID:NA
- SUG:NA
- DESC:openEuler Debranding

* Tue Aug 20 2019 huangzheng <huangzheng22@huawei.com> - 2.1.0-26
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:rename patches

* Wed Jun 12 2019 zhangyujing<zhangyujing1@huawei.com> - 2.1.0-25.h1
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:remove rpath
- Package init
