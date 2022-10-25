Name:          acl
Version:       2.3.1
Release:       1
Summary:       Commands for manipulating POSIX access control lists

License:       GPLv2+
URL:           https://savannah.nongnu.org/projects/acl
Source0:       http://download.savannah.nongnu.org/releases/acl/%{name}-%{version}.tar.gz
Source1:       http://download.savannah.nongnu.org/releases/acl/%{name}-%{version}.tar.gz.sig
#From https://savannah.nongnu.org/people/viewgpg.php?user_id=15000
Source2:       agruen-key.gpg

BuildRequires: libattr-devel gawk libtool gettext

%description
This package contains commands for manipulating POSIX access control lists,
and the libacl.so dynamic library which contains the POSIX 1003.1e draft
standard 17 functions for manipulating access control lists.

%package -n libacl
Summary: Library for supporting access control list
License: LGPLv2+
Conflicts: filesystem < 3

%description -n libacl
This package contains the library for manipulating access control list.

%package -n libacl-devel
Summary:       Files necessary to develop applications with libacl
License:       LGPLv2+
Requires:      libacl = %{version}-%{release}, libattr-devel
Obsoletes:     acl-devel < %{version}-%{release}

%description -n libacl-devel
This package contains header files for the POSIX ACL library.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure
%make_build

%install
%make_install
%delete_la_and_a
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*

%find_lang %{name}

%check
# permissions.test needs 'daemon' users to be in the 'bin' group. If not, stop this test.
if test 0 = "$(id -u)"; then
    sed -e 's|test/root/permissions.test||' -i test/Makemodule.am Makefile.in Makefile
fi
# setfacl.test needs 'bin' users to have the access to build dir. If not, stop this test.
if ! runuser -u bin -- "${PWD}/setfacl" --version; then
    sed -e 's|test/root/setfacl.test||' -i test/Makemodule.am Makefile.in Makefile
fi

%make_build check

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license doc/COPYING*
%{_bindir}/*acl

%files -n libacl
%{_libdir}/libacl.so.*

%files -n libacl-devel
%defattr(-,root,root)
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h
%{_libdir}/libacl.so
%{_libdir}/pkgconfig/libacl.pc

%files help
%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*

%changelog
* Tue Jul 27 2021 panxiaohe <panxiaohe@huawei.com> - 2.3.1-1
- Update to 2.3.1

* Fri Feb 28 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.2.53-7
- Obsoletes acl-devel

* Wed Feb 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.2.53-6
- Change acl-devel to libacl-devel

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.2.53-5
- Add libacl package

* Sat Dec 14 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.2.53-4
- Provides arch releated rpm

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.2.53-3
- Package init

