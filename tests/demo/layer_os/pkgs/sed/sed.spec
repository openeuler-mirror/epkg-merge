Name:	 sed
Version: 4.8
Release: 2
Summary: non-interactive command-line text editor

License: GPLv3+
URL:	 https://www.gnu.org/software/sed/
Source0: http://ftp.gnu.org/gnu/sed/%{name}-%{version}.tar.xz

Patch1:  backport-sed-c-flag.patch
Patch2:  backport-sed-handle-very-long-execution-lines-tiny-change.patch
Patch3:  backport-sed-handle-very-long-input-lines-with-R-tiny-change.patch

BuildRequires: gzip automake autoconf gcc
BuildRequires: glibc-devel libselinux-devel libacl-devel perl-Getopt-Long
Provides: /bin/sed
Provides: bundled(gnulib)

%description
Sed is a non-interactive command-line text editor. A stream editor is used
to per-form basic text transformations on an input stream (a file or input
from a pipeline).

%package        help
Summary:        Documents for %{name}
Buildarch:      noarch
Requires:	man info

%description help
Man pages and other related documents for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --without-included-regex
make %{?_smp_mflags}

%install
%make_install
%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%{_bindir}/sed

%files help
%doc ABOUT-NLS AUTHORS BUGS ChangeLog* INSTALL NEWS README THANKS
%{_infodir}/*.info.gz
%exclude %{_infodir}/dir*
%{_mandir}/man1/*.1.gz

%changelog
* Mon Feb 8 2021 yangzhuangzhuang<yangzhuangzhuang1@huawei.com> - 4.8-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:backport patches from upstream

* Thu Apr 16 2020 chengquan<chengquan3@huawei.com> - 4.8-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:upgrade software to v4.8

* Tue Jan  7 2020 JeanLeo<liujianliu.liu@huawei.com> - 4.7-0
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:update software to version 4.7

* Fri Aug 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.5-3
- Package init
