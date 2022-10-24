Name:           xz
Version:        5.2.5
Release:        3
Summary:        A free general-purpose data compreession software with LZMA2 algorithm
License:        Public Domain, LGPLv2.1 and GPLv2+
URL:            http://tukaani.org/xz
Source0:        http://tukaani.org/%{name}/%{name}-%{version}.tar.xz
Source1:        colorxzgrep.sh
Source2:        colorxzgrep.csh

Patch6000:      backport-CVE-2022-1271.patch

BuildRequires:  perl-interpreter gcc

Requires:       %{name} = %{version}-%{release}
Requires:       grep >= 2.20-5

%description
XZ Utils is free general-purpose data compression software with a high compression ratio.
XZ Utils were written for POSIX-like systems, but also work on some not-so-POSIX systems. XZ Utils are the successor to LZMA Utils.

The core of the XZ Utils compression code is based on LZMA SDK, but it has been modified quite a lot to be suitable for XZ Utils.
The primary compression algorithm is currently LZMA2, which is used inside the .xz container format. With typical files, XZ Utils create 30% smaller output than gzip and 15% smaller output than bzip2.

%package        devel
Summary:        Libraries & headers for xz
Requires:       %{name} = %{version}-%{release}
Provides:       xz-static
Obsoletes:      xz-static

%description    devel
This package mainly includes the following contents: static library,
the header file, example, tests use case, other development and use of content.

%package lzma-compat
Summary:        Old LZMA format compatibility binaries
Requires:       %{name} = %{version}-%{release}
Provides:       lzma = %{version}
Obsoletes:      lzma < %{version}

%description lzma-compat
This package contains the compatibility binaries for older LZMA.

%package        libs
Summary:        Libraries for xz
Obsoletes:      %{name}-compat-libs < %{version}-%{release}

%description    libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package        help
Summary:        Help documentation related to xz
BuildArch:      noarch

%description    help
This package includes help documentation and manuals related to xz.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%install
%make_install

# config color alias for xz*grep
%global profiledir %{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE1} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE2} %{buildroot}%{profiledir}

%find_lang %name

%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%files -f %{name}.lang
%defattr(-,root,root)
%doc %{_pkgdocdir}
%license %{_pkgdocdir}/COPYING*
%{_bindir}/*xz*
%{profiledir}/*

%exclude %_pkgdocdir/examples*
%exclude %{_libdir}/*.la

%files libs
%{_libdir}/lib*.so.5*

%files lzma-compat
%{_bindir}/*lz*

%files devel
%dir %{_includedir}/lzma
%doc %_pkgdocdir/examples*
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h

%{_libdir}/pkgconfig/liblzma.pc
%{_libdir}/liblzma.a
%{_libdir}/*.so

%files help
%{_mandir}/man1/*lz*
%{_mandir}/man1/*xz*
%{_mandir}/de/man1/*lz*
%{_mandir}/de/man1/*xz*

%changelog
* Fri Sep 23 2022 wangjiang <wangjiang37@h-partners.com> - 5.2.5-3
- Type:enhancement
- CVE:NA
- SUG:NA
- DESC:config color alias for xz*grep

* Fri Apr 15 2022 liudabo <liudabo1@h-partners.com> - 5.2.5-2
- Type:CVE
- ID:CVE-2022-1271
- SUG:NA
- DESC:Fix CVE-2022-1271

* Thu Jul 23 2020 shixuantong <shixuantong@huawei.com> - 5.2.5-1
- Type:NA
- ID:NA
- SUG:NA
- DESC:update to  5.2.5-1

* Sat Mar 21 2020 shenyangyang<shenyangyang4@huawei.com> - 5.2.4-10
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Split xz-lzma-compat subpackage

* Mon Feb 24 2020 chengquan<chengquan3@huawei.com> - 5.2.4-9
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Split libs subpackage for xz

* Fri Feb 21 2020 chengquan<chengquan3@huawei.com> - 5.2.4-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Add necessary BuildRequire

* Mon Jan 20 2020 JeanLeo<liujianliu.liu@huawei.com> - 5.2.4-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:correct patch info

* Mon Jan 20 2020 JeanLeo<liujianliu.liu@huawei.com> - 5.2.4-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:revert the deleted patch

* Sat Jan 18 2020 JeanLeo<liujianliu.liu@huawei.com> - 5.2.4-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove useless file or patch

* Mon Sep 2 2019 dongjian<dongjian13@huawei.com> - 5.2.4-4
- Rebuild the xz and fix description
