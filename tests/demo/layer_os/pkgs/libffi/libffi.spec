Name:		libffi
Version:	3.4.2
Release:	2.h2
Summary:	A Portable Foreign Function Interface Library
License:	MIT
URL:		http://sourceware.org/libffi
Source0:	https://github.com/libffi/libffi/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:	ffi-multilib.h
Source2:	ffitarget-multilib.h

Patch6000:	backport-x86-64-Always-double-jump-table-slot-size-for-CET-71.patch
Patch6001:	backport-Fix-check-for-invalid-varargs-arguments-707.patch
 
BuildRequires:	gcc gcc-c++ dejagnu

%description
Compilers for high level languages generate code that follows certain conventions. These
conventions are necessary, in part, for separate compilation to work. One such convention
is the "calling convention". The "calling convention" is a set of assumptions made by the
compiler about where function arguments will be found on entry to a function. A "calling
convention" also specifies where the return value for a function is found.

Some programs may not know at the time of compilation what arguments are to be passed to a
function. For instance, an interpreter may be told at run-time about the number and types
of arguments used to call a given function. Libffi can be used in such programs to provide
a bridge from the interpreter program to compiled code.

The libffi library provides a portable, high level programming interface to various calling
conventions. This allows a programmer to call any function specified by a call interface
description at run-time.

FFI stands for Foreign Function Interface. A foreign function interface is the popular name
for the interface that allows code written in one language to call code written in another
language. The libffi library really only provides the lowest, machine dependent layer of a
fully featured foreign function interface. A layer must exist above libffi that handles type
conversions for values passed between the two languages.

%package	devel
Summary:	Development files for libffi
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
The devel package with header files and libraries is for developing apps which needs libffi.

%package        help
Summary:        libffi help
Requires:       info
BuildArch:      noarch

%description    help
The help package contains man files.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure \
%ifarch riscv64
	--disable-multi-os-directory \
%endif
	--disable-static --disable-exec-static-tramp
	
%make_build

%install
%make_install
%delete_la

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%ldconfig_scriptlets

%check
%make_build check

%post help
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/libffi.info.gz || :

%preun help
if [ $1 = 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/libffi.info.gz || :
fi

%files
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/ffi*.h
%{_libdir}/*.so

%files help
%{_mandir}/man3/*.gz
%{_infodir}/libffi.info.gz

%changelog
* Mon Jul 25 2022 chenziyang<chenziyang4@huawei.com> - 3.4.2-2.h2
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:backport patches from upstream
 
* Tue Mar 15 2022 panxiaohe<panxh.life@foxmail.com> - 3.4.2-2
- delete useless old version dynamic library

* Fri Dec 3 2021 panxiaohe<panxiaohe@huawei.com> - 3.4.2-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update version to 3.4.2

* Thu Jul 22 2021 panxiaohe<panxiaohe@huawei.com> - 3.3-11
- remove unnecessary BuildRequires: gdb

* 20201125083007628982 patch-tracking 3.3-10
- append patch file of upstream repository from <e70bf987daa7b7b5df2de7579d5c51a888e8bf7d> to <e70bf987daa7b7b5df2de7579d5c51a888e8bf7d>

* Thu Jul 23 2020 Zhipeng Xie<xiezhipeng1@huawei.com> - 3.3-9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix URL

* Sat May 28 2020 whoisxxx<zhangxuzhou4@huawei.com> - 3.3-8
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Disable multi os directory to avoid compile failure for RISC-V

* Sat Mar 21 2020 chengquan<chengquan3@huawei.com> - 3.3-7
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add necessary BuildRequires

* Mon Jan 20 2020 chengquan<chengquan3@huawei.com> - 3.3-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Remove temporary dynamic library solution

* Wed Jan 15 2020 chengquan<chengquan3@huawei.com> - 3.3-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:fixbug in python3 installation

* Wed Jan 15 2020 chengquan<chengquan3@huawei.com> - 3.3-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:remove dynamic library from main package

* Tue Jan 14 2020 chengquan<chengquan3@huawei.com> - 3.3-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update dynamic library

* Tue Jan 14 2020 chengquan<chengquan3@huawei.com> - 3.3-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:fix bug in update dynamic library

* Wed Jan 8 2020 chengquan<chengquan3@huawei.com> - 3.3-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update software to 3.3

* Fri Oct 11 2019 hanzhijun<hanzhijun1@huawei.com> - 3.2.1-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update to 3.2.1

* Mon Sep 09 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.1-19
- Package init
