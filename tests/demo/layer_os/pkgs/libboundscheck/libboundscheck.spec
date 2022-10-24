%define debug_package %{nil}
Name:           libboundscheck
Version:	v1.1.11
Release:        6
License:        Mulan PSL v2
Summary:	Enhanced safety functions
Url:		https://gitee.com/openeuler/libboundscheck
Source:		https://gitee.com/openeuler/libboundscheck/repository/archive/%{name}-%{version}.tar.gz

#Dependency
BuildRequires:	gcc make rpm-build

Requires:	glibc

%description
libboundscheck provides a set of functions of 
the common memory/string operation classes.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}/ 
mkdir -p %{buildroot}%{_includedir}/
cp lib/*.so %{buildroot}%{_libdir}/
cp include/securec.h %{buildroot}%{_includedir}/
cp include/securectype.h %{buildroot}%{_includedir}/

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-,root,root)
%{_libdir}/libboundscheck.so
%{_includedir}/securec.h
%{_includedir}/securectype.h
%doc README.md
%license LICENSE

%changelog
* Sat May 08 2021 Plus_Liu <plusworld97@outlook.com> - v1.1.11-1
- Update Version.
* Mon Jun 22 2020 Guoshuai Sun <sunguoshuai@huawei.com> - v1.1.10-2
- Fix build error.
