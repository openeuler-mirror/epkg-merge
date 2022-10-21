%{!?_licensedir:%global license %%doc}
Name:    attr
Version: 2.5.1
Release: 2
Summary: Commands for Manipulating Filesystem Extended Attributes
License: GPLv2+ AND LGPLv2+
URL:     https://savannah.nongnu.org/projects/attr
Source0: https://download-mirror.savannah.gnu.org/releases/attr/attr-%{version}.tar.gz

# fix test-suite failure with perl-5.26.0 (#1473853)
Patch1:  0001-bypass-wrong-output-when-enabled-selinux.patch
Patch2:  0002-dont-skip-security.evm-when-copy-xattr.patch

BuildRequires: gettext, libtool, chrpath, gcc, 
Provides:      libattr
Obsoletes:     libattr
Conflicts:     xfsdump < 3.1.8
Conflicts:     filesystem < 3

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n libattr-devel
License: LGPLv2+
Summary: Header files for libattr
Obsoletes: libattr
Requires: glibc-headers

%description -n libattr-devel
This package contains header files and documentation needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

%package help
Summary: Including man files for attr
Requires: man

%description    help
This contains man files for the using of attr

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install
# remove rpath
chrpath -d $RPM_BUILD_ROOT%{_bindir}/attr
chrpath -d $RPM_BUILD_ROOT%{_bindir}/getfattr
chrpath -d $RPM_BUILD_ROOT%{_bindir}/setfattr


# handle docs on our own
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*

# temporarily provide attr/xattr.h symlink until users are migrated (#1601482)
ln -fs ../sys/xattr.h $RPM_BUILD_ROOT%{_includedir}/attr/xattr.h

%find_lang %{name}

%check
if ./setfattr -n user.name -v value .; then
    make check || exit $?
else
    echo '*** xattrs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi

%post -n %{name} -p /sbin/ldconfig
%postun -n %{name} -p /sbin/ldconfig

%files -f %{name}.lang
%doc doc/CHANGES
%license doc/COPYING*
%{_bindir}/*
%{_libdir}/libattr.so.*
%config(noreplace) %{_sysconfdir}/xattr.conf

%files -n libattr-devel
%{_libdir}/libattr.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libattr.a
%{_libdir}/libattr.la
%{_includedir}/attr

%files help
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Mon Jan 24 2022 volcanodragon <linfeilong@huawei.com> - 2.5.1-2
- dont skip security.evm copy for ima

* Tue Nov 16 2021 Wenchao Hao <haowenchao@huawei.com> - 2.5.1-1
- Update to attr-2.5.1

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 2.4.48-14
- DESC: delete -Sgit from %autosetup, and delete BuildRequires git

* Fri Jul 23 2021 zhouwenpei <zhouwenpei1@huawei.com> - 2.4.48-13
- remove useless buildrequires 

* Wed Sep 2 2020 Anakin Zhang <benjamin93@163.com> - 2.4.48-12
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: carry security.evm when copying files

* Sun Jul 12 2020 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 2.4.48-11
- backport upstream bugfix patches

* Wed Jun 29 2020 Markeryang <yanglongkang@163.com> - 2.4.48-10
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: make check add judgment condition

* Mon Jun 29 2020 Zhiqiang Liu <lzhq28@mail.ustc.edu.cn> - 2.4.48-9
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: renumber patches

* Fri Mar 20 2020 hy-euler <eulerstoragemt@huawei.com> - 2.4.48-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: the building requires the gdb

* Mon Mar 16 2020 Shijie Luo<luoshijie1@huawei.com> - 2.4.48-7
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix error condition of while loop 
       in 0001-bypass-wrong-output-when-enabled-selinux.patch.

* Mon Mar 16 2020 Shijie Luo<luoshijie1@huawei.com> - 2.4.48-6
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:add patch to bypass selinux messages.

* Fri Aug 30 2019 zoujing<zoujing13@huawei.com> - 2.4.48-5
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESCi:openEuler Debranding

* Tue Aug 20 2019 zoujing<zoujing13@huawei.com> - 2.4.48-4
- Type:enhancemnet
- ID:NA
- SUG:NA
- DESCi:openEuler Debranding

* Tue Aug 20 2019 luoshijie<luoshijie1@huawei.com> - 2.4.48-2.3
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:rename patch name

* Wed Jun 12 2019 gulining<gulining1@huawei.com> - 2.4.48-2.2
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:remove rpath

* Wed Apr 24 2019 tianhang<tianhang1@huawei.com>- 2.4.48-2.1
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:Switch back to syscall

* Mon Apr 15 2019 Buildteam <buildteam@openeuler.org> - 2.4.48-2
- Package Initialization
