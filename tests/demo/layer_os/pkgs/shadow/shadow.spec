Name: shadow
Version: 4.9
Release: 4
Epoch: 2
License: BSD and GPLv2+
Summary: Tools for managing accounts and shadow password files
URL: http://pkg-shadow.alioth.debian.org/
Source0: https://github.com/shadow-maint/shadow/releases/download/v%{version}/shadow-%{version}.tar.xz
Source2: shadow-utils.useradd
Source3: shadow-utils.login.defs
Source4: shadow-bsd.txt
Source5: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
Source6: chpasswd
Source7: newusers

%global includesubiddir %{_includedir}/shadow

# fix unknown item 'LASTLOG_MAX_UID'
Patch0:  shadow-4.8-goodname.patch
Patch1:  shadow-4.9-null-tm.patch
Patch2:  shadow-4.8-long-entry.patch
Patch3:  usermod-unlock.patch
Patch4:  useradd-create-directories-after-the-SELinux-user.patch
Patch5:  shadow-4.1.5.1-var-lock.patch
Patch6:  shadow-utils-fix-lock-file-residue.patch
Patch7:  Makefile-include-libeconf-dependency-in-new-idmap.patch 
Patch8:  usermod-allow-all-group-types-with-G-option.patch
Patch9:  useradd-avoid-generating-an-empty-subid-range.patch
Patch10: libmisc-fix-default-value-in-SHA_get_salt_rounds.patch
Patch11: semanage-close-the-selabel-handle.patch
Patch12: Revert-useradd.c-fix-memleaks-of-grp.patch
Patch13: useradd-change-SELinux-labels-for-home-files.patch
Patch14: libsubid-link-to-PAM-libraries.patch
Patch15: Fix-out-of-tree-builds-with-respect-to-libsubid-incl.patch
Patch16: Respect-enable-static-no-in-libsubid.patch
Patch17: Fixes-the-linking-issues-when-libsubid-is-static-and.patch
Patch18: pwck-fix-segfault-when-calling-fprintf.patch
Patch19: newgrp-fix-segmentation-fault.patch
Patch20: groupdel-fix-SIGSEGV-when-passwd-does-not-exist.patch
Patch21: backport-useradd-modify-check-ID-range-for-system-users.patch
Patch22: shadow-add-sm3-crypt-support.patch

BuildRequires: gcc, libselinux-devel, audit-libs-devel, libsemanage-devel
BuildRequires: libacl-devel, libattr-devel
BuildRequires: bison, flex, gnome-doc-utils, docbook-style-xsl, docbook-dtds
BuildRequires: autoconf, automake, libtool, gettext-devel, itstool, pam-devel
Requires: libselinux
Requires: audit-libs
Requires: setup
Requires(pre): coreutils
Requires(post): coreutils
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: shadow-utils
Obsoletes: shadow-utils

%description
This package includes the necessary programs for converting plain
password files to the shadow password format and to manage user and
group accounts.

%package subid-devel
Summary: Development package for shadow-utils-subid
License: BSD and GPLv2+

%description subid-devel
Development files for shadow-utils-subid.

%package_help

%prep
%autosetup -n shadow-%{version} -p1

iconv -f ISO88591 -t utf-8  doc/HOWTO > doc/HOWTO.utf8
cp -f doc/HOWTO.utf8 doc/HOWTO

cp -a %{SOURCE4} %{SOURCE5} .

%build
export CFLAGS="$RPM_OPT_FLAGS -fpie"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"

autoreconf -fiv
%configure \
        --enable-shadowgrp \
        --enable-man \
        --with-audit \
        --with-sha-crypt \
        --with-selinux \
        --without-libcrack \
        --with-libpam \
        --enable-shared \
        --with-group-name-max-length=32
%make_build

%install
rm -rf $RPM_BUILD_ROOT
%make_install gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale MKINSTALLDIRS=`pwd`/mkinstalldirs
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}/default
install -p -c -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/login.defs
install -p -c -m 0600 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/default/useradd
install -p -c -m 0644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/chpasswd
install -p -c -m 0644 %{SOURCE7} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/newusers

ln -s useradd $RPM_BUILD_ROOT%{_sbindir}/adduser
ln -s useradd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/adduser.8
for subdir in $RPM_BUILD_ROOT/%{_mandir}/{??,??_??,??_??.*}/man* ; do
        test -d $subdir && test -e $subdir/useradd.8 && echo ".so man8/useradd.8" > $subdir/adduser.8
done

# Remove binaries we don't use.
rm $RPM_BUILD_ROOT/%{_bindir}/chfn
rm $RPM_BUILD_ROOT/%{_bindir}/chsh
rm $RPM_BUILD_ROOT/%{_bindir}/expiry
rm $RPM_BUILD_ROOT/%{_bindir}/groups
rm $RPM_BUILD_ROOT/%{_bindir}/login
rm $RPM_BUILD_ROOT/%{_bindir}/passwd
rm $RPM_BUILD_ROOT/%{_bindir}/su
rm $RPM_BUILD_ROOT/%{_bindir}/faillog
rm $RPM_BUILD_ROOT/%{_sbindir}/logoutd
rm $RPM_BUILD_ROOT/%{_sbindir}/nologin
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/man3/getspnam.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man3/getspnam.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/faillog.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/faillog.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/faillog.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/faillog.*
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/chfn
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/chsh
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/login
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/passwd
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/su

find $RPM_BUILD_ROOT%{_mandir} -depth -type d -empty -delete
%find_lang shadow
for dir in $(ls -1d $RPM_BUILD_ROOT%{_mandir}/{??,??_??}) ; do
    dir=$(echo $dir | sed -e "s|^$RPM_BUILD_ROOT||")
    lang=$(basename $dir)
done

# Move subid.h to its own folder
echo $(ls)
mkdir -p $RPM_BUILD_ROOT/%{includesubiddir}
install -m 644 libsubid/subid.h $RPM_BUILD_ROOT/%{includesubiddir}/

# Remove .la files created by libsubid
rm -f $RPM_BUILD_ROOT/%{_libdir}/libsubid.la

%files -f shadow.lang
%doc NEWS doc/HOWTO README
%{!?_licensedir:%global license %%doc}
%license gpl-2.0.txt shadow-bsd.txt
%attr(0644,root,root)   %config(noreplace) %{_sysconfdir}/login.defs
%attr(0644,root,root)   %config(noreplace) %{_sysconfdir}/default/useradd
%{_bindir}/sg
%attr(4755,root,root) %{_bindir}/chage
%attr(4755,root,root) %{_bindir}/gpasswd
%{_bindir}/lastlog
%attr(4755,root,root) %{_bindir}/newgrp
%attr(4755,root,root) %{_bindir}/newgidmap
%attr(4755,root,root) %{_bindir}/newuidmap
%{_sbindir}/adduser
%attr(0755,root,root)   %{_sbindir}/user*
%attr(0755,root,root)   %{_sbindir}/group*
%{_sbindir}/grpck
%{_sbindir}/pwck
%{_sbindir}/*conv
%{_sbindir}/chpasswd
%{_sbindir}/chgpasswd
%{_sbindir}/newusers
%{_sbindir}/vipw
%{_sbindir}/vigr
%{_sysconfdir}/pam.d/chpasswd
%{_sysconfdir}/pam.d/groupmems
%{_sysconfdir}/pam.d/newusers

%files subid-devel
%{_libdir}/libsubid.so.*
%{includesubiddir}/subid.h
%{_libdir}/libsubid.so

%files help
%{_mandir}/*/*

%changelog
* Tue Aug 2 2022 zhengxiaoxiao <zhengxiaoxiao2@huawei.com> - 2:4.9-4
- add-sm3-crypt-support.patch add update release to 4.9-4

* Mon Feb 21 2022 panxiaohe <panxh.life@foxmail.com> - 2:4.9-1
- update to 4.9
- synchronized login.defs with upstream file
- useradd: modify check ID range for system users

* Thu Sep 30 2021 steven Y.Gui <steven_ygui@163.com> - 2:4.8.1-7
- backport some patches to fix memory leak

* Mon Jul 26 2021 wangchen<wangchen137@huawei.com> - 2:4.8.1-6
- delete unnecessary gdb from BuildRequires

* Thu Apr 29 2021 Hugel<gengqihu1@huawei.com> - 2:4.8.1-5
- shadow should depend on audit-libs

* Thu Jul 9 2020 Anakin Zhang<benjamin93@163.com> - 2:4.8.1-4
- fix zh_CN typo

* Sun Jun 28 2020 Anakin Zhang<benjamin93@163.com> - 2:4.8.1-3
- generate /var/spool/mail/$USER with the proper SELinux user identity

* Tue May 12 2020 steven<steven_ygui@163.com> - 2:4.8.1-2
- Enable --with-libpam config during compiling

* Fri Apr 24 2020 steven<steven_ygui@163.com> - 2:4.8.1-1
- Upgrade version to 4.8.1

* Sat Mar 21 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-10
- Only package man file into shadow-help; add buildrequires of gdb

* Tue Mar 17 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-9
- Remove redundant file

* Fri Feb 21 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-8
- Remove redundant patches

* Thu Feb 6 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-7
- User name can start with an upper case letter

* Sat Jan 18 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-6
- Delete ALWAYS_SET_PATH, which has been set by security-tool

* Thu Jan 16 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-5
- Fix unknown item 'LASTLOG_MAX_UID'

* Sun Jan 12 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-4
- Delete unused patch

* Thu Dec 19 2019 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-3
- Delete unused infomation

* Mon Dec 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 2:4.7-2
- fix invaild path

* Thu Aug 29 2019 hexiaowen <hexiaowen@huawei.com> - 2:4.7-1
- update to 4.7

* Tue Aug 20 2019 guoxiaoqi<guoxiaoqi2@huawei.com> - 2:4.6-2.h9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:rename patches

* Thu Aug 8 2019 guoxiaoqi <guoxiaoqi2@huawei.com> - 2:4.6-2.h8
- Type:NA
- ID:NA
- SUG:NA
- DESC: format patches

* Thu Aug 1 2019 Jiangchuangang<Jiangchuangang@huawei.com> - 2:4.6-2.h7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:openEuler Debranding

* Fri May 3 2019 lubing<lubing6@huawei.com> - 2:4.6-2.h6
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix lock file residue

* Tue Mar 12 2019 yangzhuangzhuang<yangzhuangzhuang1@huawei.com> - 2:4.6-2.h5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:su.c: run pam_getenvlist() after setup_env
       Log UID in nologin
       Fix some issues found in Coverity scan.
       useradd: fix segfault trying to overwrite const data with mkstemp
       Fix the default mentioned in man page for SUB_UID/GID_COUNT variables.

* Wed Mar 6 2019 hanzhijun<hanzhijun@huawei.com> - 2:4.6-2.h4
- Type:bugfix
- ID:NA
- SUG:NA
  DESC:shadow 4.1.5.1 var lock

* Thu Jan 31 2019 liuqianya<liuqianya@huawei.com> - 2:4.6-2.h3
- Type:bugfix
- ID:NA
- SUG:NA
  DESC:Revert"shadow 4.1.5.1 var lock"

* Mon Jan 28 2019 liuqianya<liuqianya@huawei.com> - 2:4.6-2.h2
- Type:bugfix
- ID:NA
- SUG:NA
  DESC:Revert "shadow-utils: sync patches"

* Fri Jan 25 2019 liuqianya<liuqianya@huawei.com> - 2:4.6-2.h1
- Type:bugfix
- ID:NA
- SUG:NA
  DESC:add ruserok to avoid compilation failure
      hulk shadow remove passwd param for useradd
      shadow 4.1.5.1 var lock

* Sat Jul 14 2018 Jiangchuangang<Jiangchuangang@huawei.com> - 2:4.6-2
- Package Initialization
