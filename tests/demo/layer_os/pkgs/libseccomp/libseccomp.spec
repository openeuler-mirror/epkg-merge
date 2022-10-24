Name:		libseccomp
Version:	2.5.3
Release:        2
Summary:	Interface to the syscall filtering mechanism
License:	LGPLv2
URL:		https://github.com/seccomp/libseccomp
Source0:	https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz

Patch0:         backport-bpf-pfc-Add-handling-for-0-syscalls-in-the-binary-tr.patch
Patch1:         backport-tests-Add-a-binary-tree-test-with-zero-syscalls.patch

BuildRequires:	gcc gperf autoconf automake

%description
The libseccomp library provides an easy to use, platform independent, interface to
the Linux Kernel's syscall filtering mechanism. The libseccomp API is designed to
abstract away the underlying BPF based syscall filter language and present a more
conventional function-call based filtering interface that should be familiar to,
and easily adopted by, application developers.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}
Obsoletes:      %{name}-static <= %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf
%configure
%make_build

%install
%make_install
%delete_la

%check
make check

%pre

%preun

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc CREDITS
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%{_bindir}/scmp_sys_resolver
%{_includedir}/seccomp.h
%{_includedir}/seccomp-syscalls.h
%{_libdir}/%{name}.a
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files help
%doc CHANGELOG CONTRIBUTING.md README.md
%{_mandir}/man*/*

%changelog
* Sat Aug 27 2022 zoulin <zoulin13@h-partners.com> - 2.5.3-2
- backport patches from upstream

* Tue Dec 28 2021 fuanan <fuanan3@huawei.com> - 2.5.3-1
- update version to 2.5.3

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 2.5.1-3
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Tue Jul 20 2021 fuanan <fuanan3@huawei.com> - 2.5.1-2
- Remove redundant gdb from BuildRequires

* Mon Jan 25 2021 wangchen <wangchen137@huawei.com> - 2.5.1-1
- update to 2.5.1

* Mon Jul 27 2020 Hugel <gengqihu1@huawei.com> - 2.5.0-1
- update to 2.5.0

* Tue Jun 30 2020 Liquor <lirui130@huawei.com> - 2.4.3-2
- add the patch of support for RISC-V

* Fri Apr 24 2020 BruceGW <gyl93216@163.com> - 2.4.3-1
- update upstream to 2.4.3

* Fri Oct 11 2019 jiangchuangang <jiangchuangang@huawei.com> - 2.4.1-3
- Type: enhancement
- ID: NA
- SUG: NA
- DESC: remove so.* from devel

* Tue Sep 24 2019 luhuaxin <luhuaxin@huawei.com> - 2.4.1-2
- Type: enhancement
- ID: NA
- SUG: NA
- DESC: add help package and merge static package

* Fri Aug 16 2019 luhuaxin <luhuaxin@huawei.com> - 2.4.1-1
- Package init
