Name:		popt
Version:	1.18
Release:        3
Summary:	C library for parsing command line parameters
License:	MIT
URL:		https://github.com/rpm-software-management/popt/
Source0:        http://ftp.rpm.org/%{name}/releases/%{name}-1.x/%{name}-%{version}.tar.gz

Patch0: 	fix-obscure-iconv-mis-call-error-path-could-lead-to-.patch
Patch1: 	fix-handle-newly-added-asset-.-call-like-elsewhere.patch
Patch2: 	fix-permit-reading-aliases-remove-left-over-goto-exi.patch
Patch3: 	fix-coverity-CID-1057440-Unused-pointer-value-UNUSED.patch
Patch4: 	backport-Consider-POPT_CONTEXT_KEEP_FIRST-during-reset.patch
Patch5: 	backport-Fix-incorrect-handling-of-leftovers-with-poptStuffAr.patch

BuildRequires:	gcc git gettext

%description
The popt library exists essentially for parsing command line options. Some
specific advantages of popt are no global variables (allowing multiple passes
in parsing argv), parsing an arbitrary array of argv-style elements (allowing
parsing of command-line-strings from any source), a standard method of option
aliasing, ability to exec external option filters, and automatic generation
of help and usage messages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:	pkgconfig
Provides:	%{name}-static = %{version}-%{release}
Obsoletes:	%{name}-static < %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	help
Summary: 	Doc files for %{name}
Buildarch:	noarch

%description 	help
The %{name}-help package contains doc files for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}/%{_libdir}/libpopt.la
mkdir -p %{buildroot}/%{_sysconfdir}/popt.d

%find_lang %{name}

%check
make check

%pre

%preun

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%{_sysconfdir}/%{name}.d
%{_libdir}/lib%{name}.so*

%files devel
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.a

%files help
%doc CHANGES README
%{_mandir}/man3/%{name}.3.gz

%changelog
* Thu Aug 18 2022 zhangruifang <zhangruifang1@h-partners.com> - 1.18-3
- Revert fix memory leak regressions in popt

* Mon Aug 15 2022 panxiaohe <panxh.life@foxmail.com> - 1.18-2
- Fix incorrect handling of leftovers with poptStuffArgs and memory leak

* Sat Jul 25 2020 zhangxingliang <zhangxingliang3@huawei.com> - 1.18-1
- Type:update
- ID:NA
- SUG:NA
- DESC:update to 1.18

* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.16-17
- Strenthen spec

* Fri Aug 30 2019 luhuaxin <luhuaxin@huawei.com> - 1.16-16
- Package init
