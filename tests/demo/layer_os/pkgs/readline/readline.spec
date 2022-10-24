Name:	 readline
Version: 8.1
Release: 1
Summary: Readline library for editing typed command lines

License: GPLv3+
URL:	 http://tiswww.case.edu/php/chet/readline/rltop.html
Source0: http://git.savannah.gnu.org/cgit/readline.git/snapshot/%{name}-%{version}.tar.gz

Patch0:  readline-8.0-shlib.patch

BuildRequires:	gcc gcc-c++ ncurses-devel

%description
The GNU Readline library provides a set of functions for use by
applications that allow users to edit command lines as they are
typed in. Both Emacs and vi editing modes are available.The Readline
library includes additional functions to maintain a list of
previously-entered command lines, to recall and perhaps reedit those
lines, and perform csh-like history expansion on previous commands.

%package devel
Summary:  Development Header files for readline library
Requires: %{name} = %{version}-%{release}
Requires: ncurses-devel
Provides: %{name}-static
Obsoletes: %{name}-static

%description devel
The GNU Readline library provides a set of functions for use by
applications that allow users to edit command lines as they are
typed in.

This package contains Development header files for the readline
library.

%package        help
Summary:        Documents for %{name}
Buildarch:      noarch
Requires:	man info

%description help
Man pages and other related documents for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
export CPPFLAGS="-I%{_includedir}/ncurses"
%configure --with-curses
%make_build

%install
%make_install

%ldconfig_scriptlets

%files
%doc
%license COPYING USAGE
%{_libdir}/libhistory.so.*
%{_libdir}/libreadline.so.*

%files devel
%{_includedir}/%{name}/*.h
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%{_libdir}/pkgconfig/%{name}.pc
%{_docdir}/%{name}/*
%{_datadir}/%{name}
%{_libdir}/*.a

%files help
%{_infodir}/history.info*
%{_infodir}/rluserman.info*
%{_infodir}/readline.info*
%exclude %{_infodir}/dir*
%{_mandir}/man3/*.3.gz


%changelog
* Mon Sep 27 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 8.1-1
- update to 8.1

* Thu Jun 24 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 8.0-3
- Delete useless old version dynamic library

* Wed Dec 9 2020 zoulin <zoulin13@huawei.com> - 8.0-2
- Modify URL

* Mon Jul 13 2020 wangchen <wangchen137@huawei.com> - 8.0-1
- update to 8.0

* Thu Aug 22 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.0-13
- Package init
