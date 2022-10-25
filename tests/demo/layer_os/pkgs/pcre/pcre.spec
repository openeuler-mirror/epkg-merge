Name:		pcre
Version:	8.45
Release:        2
Summary:	Perl Compatible Regular Expressions
## Source package only:
# INSTALL:                  FSFAP
# install-sh:               MIT and Public Domain
# ltmain.sh:                (GPLv2+ or BSD) and (GPLv3+ or MIT)
# missing:                  GPLv2+ or BSD
# compile:                  GPLv2+ or BSD
# config.sub:               GPLv3+ or BSD
# m4/ax_pthread.m4:         GPLv3+ with exception
# m4/libtool.m4:            GPLv2+ or BSD
# m4/ltversion.m4:          FSFULLR
# m4/pcre_visibility.m4:    FSFULLR
# m4/lt~obsolete.m4:        FSFULLR
# m4/ltsugar.m4:            FSFULLR
# m4/ltoptions.m4:          FSFULLR
# aclocal.m4:               (GPLv2+ or BSD) and FSFULLR 
# Makefile.in:              FSFULLR
# configure:                FSFUL
# test-driver:              GPLv2+ with exception
# testdata:                 Public Domain (see LICENSE file)
## Binary packages:
# other files:              BSD
License:	BSD
URL:		http://www.pcre.org/
Source0:	https://ftp.pcre.org/pub/pcre/%{name}-%{version}.tar.bz2


BuildRequires:	readline-devel autoconf automake coreutils	
BuildRequires:	gcc gcc-c++ glibc-common libtool make
BuildRequires:	bash diffutils grep
Provides:	%{name}-utf16 = %{version}-%{release} %{name}-utf32 = %{version}-%{release}
Provides:       %{name}-cpp = %{version}-%{release} %{name}-tools = %{version}-%{release}
Obsoletes:	%{name}-utf16 < %{version}-%{release} %{name}-utf32 < %{version}-%{release}
Obsoletes:      %{name}-cpp < %{version}-%{release} %{name}-tools < %{version}-%{release}

%description
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl 5. PCRE has
its own native API, as well as a set of wrapper functions that correspond
to the POSIX regular expression API. The PCRE library is free, even for
building proprietary software.

PCRE was originally written for the Exim MTA, but is now used by many
high-profile open source projects, including Apache, PHP, KDE, Postfix,
and Nmap. PCRE has also found its way into some well known commercial
products, like Apple Safari. Some other interesting projects using PCRE
include Chicken, Ferite, Onyx, Hypermail, Leafnode, Askemos, Wenlin, and
8th.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}
Obsoletes:      %{name}-static < %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	help
Summary: 	Doc files for %{name}
Buildarch:	noarch
Requires:	man

%description 	help
The %{name}-help package contains doc files for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
libtoolize -cf
autoreconf -vif
%configure \
%ifarch riscv64
	--disable-jit \
%else
	--enable-jit \
%endif
	--enable-pcretest-libreadline --enable-utf \
	--enable-unicode-properties --enable-pcre8 --enable-pcre16 \
	--enable-pcre32 --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_docdir}/pcre

%check
make check VERBOSE=yes

%ldconfig_scriptlets

%files
%doc NEWS README
%license LICENCE AUTHORS
%{_libdir}/*.so.*
%{_bindir}/pcregrep
%{_bindir}/pcretest

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_bindir}/pcre-config
%{_libdir}/*.a

%files help
%doc doc/*.txt doc/html
%doc HACKING pcredemo.c
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sat Oct 8 2022 huangduirong <huangduirong@huawei.com> - 8.45-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update the prep of spec

* Tue Feb 8 2022 yangzhuangzhuang <yangzhuangzhuang1@h-partners.com> - 8.45-1
- update to 8.45

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 8.44-2
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Thu Jul 23 2020 zhangxingliang <zhangxingliang3@huawei.com> - 8.44-1
- Type: update
- ID: NA
- SUG: NA
- DESC: update to 8.44

* Wed Jun 24 2020 xuping <xuping21@huawei.com> - 8.43-6
- Type: cves
- ID: CVE-2020-14155
- SUG: NA
- DESC: fix CVE-2020-14155

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.43-5
- Type: enhancement
- ID: NA
- SUG: NA
- DESC: remove unnecessary files

* Mon Nov 11 2019 shenyangyang <shenyangyang4@huawei.com> - 8.43-4
- Type: enhancement
- ID: NA
- SUG: NA
- DESC:modify obsoletes version

* Wed Oct 10 2019 luhuaxin <luhuaxin@huawei.com> - 8.43-3
- Type: enhancement
- ID: NA
- SUG: NA
- DESC: move AUTHORS to license folder

* Sat Sep 29 2019 luhuaxin <luhuaxin@huawei.com> - 8.43-2
- Type: enhancement
- ID: NA
- SUG: NA
- DESC: move README file to main package

* Fri Aug 20 2019 luhuaxin <luhuaxin@huawei.com> - 8.43-1
- Package init
