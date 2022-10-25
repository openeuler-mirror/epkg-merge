Name:    grep
Version: 3.7
Release: 7
Summary: A string search utility
License: GPLv3+
URL: http://www.gnu.org/software/grep/
Source0: https://ftp.gnu.org/gnu/grep/grep-%{version}.tar.xz
Source1: color_grep.sh
Source2: colorgrep.csh
Source3: grepconf.sh

Patch1:  backport-grep-avoid-sticky-problem-with-f-f.patch
Patch2:  backport-grep-s-does-not-suppress-binary-file-matches.patch
Patch3:  backport-grep-work-around-PCRE-bug.patch
Patch4:  backport-grep-migrate-to-pcre2.patch
Patch5:  backport-grep-Don-t-limit-jitstack_max-to-INT_MAX.patch
Patch6:  backport-grep-speed-up-fix-bad-UTF8-check-with-P.patch
Patch7:  backport-grep-fix-minor-P-memory-leak.patch
Patch8:  backport-grep-djb2-correction.patch
Patch9:  backport-build-update-gnulib-submodule-to-latest.patch
Patch10: backport-grep-fix-bug-with-and-some-Hangul-Syllables.patch
Patch11: backport-tests-improve-tests-of.patch
Patch12: backport-grep-sanity-check-GREP_COLOR.patch
Patch13: backport-grep-fix-regex-compilation-memory-leaks.patch

BuildRequires: gcc pcre2-devel texinfo gettext libsigsegv-devel automake
Provides: /bin/egrep /bin/fgrep /bin/grep bundled(gnulib)

%description
Grep searches one or more input files for lines containing a match to
a specified pattern. By default, Grep outputs the matching lines.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --disable-silent-rules \
CPPFLAGS="-I%{_includedir}/pcre2" CFLAGS="$RPM_OPT_FLAGS -fsigned-char"
%make_build

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

install -pm 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -Dpm 755 %{SOURCE3} $RPM_BUILD_ROOT%{_libexecdir}/grepconf.sh

%pre
%preun
%post
%postun

%check
make check

%files
%{_datadir}/locale/*
%config(noreplace) %{_sysconfdir}/profile.d/color_grep.sh
%config(noreplace) %{_sysconfdir}/profile.d/colorgrep.csh
%doc NEWS README THANKS TODO
%license COPYING AUTHORS
%{_bindir}/*grep
%{_libexecdir}/grepconf.sh
%{_infodir}/grep.info.gz
%{_mandir}/man1/*grep.1.gz


%changelog
* Wed Jul 27 2022 panxiaohe <panxh.life@foxmail.com> - 3.7-7
- backport patches from upstream

* Fri Jul 15 2022 panxiaohe <panxh.life@foxmail.com> - 3.7-6
- Added coloring aliases to fgrep egrep and grep

* Tue Jun 28 2022 panxiaohe <panxh.life@foxmail.com> - 3.7-5
- grep: Don't limit jitstack_max to INT_MAX
- grep: speed up, fix bad-UTF8 check with -P
- grep: fix minor -P memory leak

* Sat May 14 2022 licihua <licihua@huawei.com> - 3.7-4
- Modify the dependency from pcre to pcre2

* Fri Mar 18 2022 yangzhuangzhuang <yangzhuangzhuang1@h-partners.com> - 3.7-3
- The -s option no longer suppresses "binary file matches" messages

* Tue Feb 8 2022 yangzhuangzhuang <yangzhuangzhuang1@h-partners.com> - 3.7-2
- avoid sticky problem with '-f - -f -'

* Wed Dec 29 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 3.7-1
- update version to 3.7

* Fri Aug 20 2021 chenyanpanHW <chenyanpan@huawei.com> - 3.6-3
- DESC: remove unnecessary BuildRequires git, add necessary BuildRequires automake

* Tue Aug 10 2021 yangzhuangzhuang<yangzhuangzhuang1@huawei.com> - 3.6-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix the compilation failure with the new version glibc-2.34

* Thu Jan 21 2021 wangchen<wangchen137@huawei.com> - 3.6-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update to 3.6

* Wed Jul 15 2020 Liquor<lirui130@huawei.com> - 3.4-1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add -fsigned-char option

* Tue Jan  7 2020 JeanLeo<liujianliu.liu@huawei.com> - 3.4-0
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:update software to version 3.4

* Mon Oct 21 2019 chengquan<chengquan3@huawei.com> - 3.1-10
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix package bug

* Mon Aug 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.1-9
- Package init

