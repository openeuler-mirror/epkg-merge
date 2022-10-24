Name: psmisc
Version: 23.4
Release: 2
Summary: Utilities for managing processes on your system
License: GPLv2+
URL: https://gitlab.com/psmisc/psmisc
Source0: https://sourceforge.net/projects/%{name}/files/%{name}/%{name}-%{version}.tar.xz

Patch6000: backport-patch-fix-checking-truncated-process-names.patch 

BuildRequires: libselinux-devel gettext ncurses-devel autoconf automake gcc 

%description
This PSmisc package is a set of some small useful utilities that use the proc
filesystem. We're not about changing the world, but providing the system
administrator with some help in common tasks.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --prefix=%{_prefix} --enable-selinux
%make_build

%install
%make_install
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/fuser $RPM_BUILD_ROOT%{_sbindir}
%find_lang %name --all-name --with-man

%files -f %{name}.lang
%{_sbindir}/fuser
%{_bindir}/*
%{_mandir}/man1/*
%license COPYING
%doc AUTHORS ChangeLog README

%changelog
* Thu Aug 11 2022 liutie <liutie4@huawei.com> - 23.4-2
- Fix checking truncated process names

* Thu Dec 2 2021 zhouwenpei <zhouwenpei1@huawei.com> - 23.4-1
- upgrade to 23.4

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 23.3-3
- DESC: delete -Sgit from %autosetup, and delete BuildRequires git

* Tue Nov 03 2020 xinghe <xinghe1@huawei.com> - 23.3-2
- sync patchs

* Thu Jul 16 2020 jinzhimin <jinzhimin2@huawei.com> - 23.3-1
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:upgrade to 23.3

* Wed May 8 2019 xiashuang <xiashuang1@huawei.com> - 23.1-5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix adapt patch error

* Tue Jan 22 2019 xiashuang <xiashuang1@huawei.com> - 23.1-4
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:adapt patches from 7.3

* Mon Sep 10 2018 openEuler Buildteam <buildteam@openeuler.org> - 23.1-3
- Package init
