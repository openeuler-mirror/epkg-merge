Name:		less
Version:	590
Release:        2
Summary:	Less is a pager that displays text files.
License:	GPLv3+ or BSD
URL:		http://www.greenwoodsoftware.com/less
Source0:	http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
Patch0:		less-394-time.patch
Patch1:		less-475-fsync.patch

BuildRequires:	gcc make ncurses-devel autoconf automake libtool

%description
Less is a pager. A pager is a program that displays text files.
Other pagers commonly in use are more and pg. Pagers are often
used in command-line environments like the Unix shell and the MS-DOS
command prompt to display files.

Less is not an editor. You can't change the contents of the file
you're viewing. Less is not a windowing system. It doesn't have
fancy scroll bars or other GUI (graphical user interface) elements.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
rm -f ./configure
autoreconf -ivf
%configure
%make_build CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"

%install
%make_install


%files
%defattr(-,root,root)
%license LICENSE COPYING
%{_bindir}/less*

%files help
%doc README NEWS INSTALL
%{_mandir}/man1/*

%changelog
* Thu Oct 13 2022 fuanan <fuanan3@h-partners.com> - 590-2
- DESC:fix the changelog exception macro

* Fri Sep 24 2021 fuanan <fuanan3@huawei.com> - 590-1
- update version to 590

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 563-3
- DESC: delete -S git from autosetup, and delete BuildRequires git

* Fri May 28 2021 fuanan <fuanan3@huawei.com> - 563-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:[add] backport patches from upstream
       Create only one ifile when a file is opened under different names.
       Remove extraneous frees, associated with removed call to lrealpath.
       Fix crash when call set_ifilename with a pointer to the name that is
       Remove unnecessary call to pshift in pappend.
       Reset horizontal shift when opening a new file.
       Protect from buffer overrun.
       Make histpattern return negative value to indicate error.
       Lesskey: don't translate ctrl-K in an EXTRA string.
       Ignore SIGTSTP in secure mode.
       Fix "Tag not found" error while looking for a tag's location
       Fix minor memory leak with input preprocessor.

* Thu Jan 21 2021 wangchen <wangchen137@huawei.com> - 563-1
- Update to 563

* Thu Jan 09 2020 openEuler Buildteam <buildteam@openeuler.org> - 551-3
- Delete unneeded files

* Fri Sep 27 2019 yefei <yefei25@huawei.com> - 551-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: delete irrelevant comment

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 551-1
- Package Init
