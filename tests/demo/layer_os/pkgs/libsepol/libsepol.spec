Name:           libsepol
Version:        3.3
Release:        2
Summary:        SELinux binary policy manipulation library
License:        LGPLv2+
URL:            https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz 

BuildRequires:  gcc flex

%description
libsepol provides an API for the manipulation of SELinux binary
policies. It is used by checkpolicy (the policy compiler) and similar
tools, as well as by programs like load_policy that need to perform
specific transformations on binary policies such as customizing
policy boolean settings.

%package devel
Summary: Header files and libraries for %{name}
Requires:%{name} = %{version}-%{release}
Provides:%{name}-static = %{version}-%{release}

%description devel
Header files and libraries for %{name}

%package_help

%prep
%autosetup -n %{name}-%{version} -p2

%build
make clean
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}"

%install
rm -rf %{buildroot}
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" install

%pre

%preun

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libsepol.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsepol.pc
%{_libdir}/*.a
%exclude %{_bindir}/chkcon

%files help
%defattr(-,root,root)
%{_mandir}/man8/*
%{_mandir}/ru/man8/*
%{_mandir}/man3/*

%changelog
* Tue Mar 15 2022 panxiaohe <panxh.life@foxmail.com> - 3.3-2
- delete useless old version dynamic library

* Thu Jan 13 2022 panxiaohe <panxiaohe@huawei.com> - 3.3-1
- update to 3.3

* Fri Dec 10 2021 panxiaohe <panxiaohe@huawei.com> - 3.1-6
- fix secilc-fuzzer issues

* Fri Sep 10 2021 panxiaohe <panxiaohe@huawei.com> - 3.1-5
- fix secilc-fuzzer issues

* Fri May 28 2021 panxiaohe <panxiaohe@huawei.com> - 3.1-4
- Drop unnecessary telinit

* Mon Mar 15 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 3.1-3
- fix heap-use-after-free in cil_yy_switch_to_buffer
- fix heap-use-after-free in __class_reset_perm_values()
- fix heap-buffer-overflow in cil_print_recursive_blockinherit

* Thu Mar 4 2021 Lirui <lirui130@huawei.com> - 3.1-2
- fix NULL pointer dereference in cil_fill_ipaddr 

* Fri Jul 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.1-1
- update to 3.1

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9-1
- Package init
