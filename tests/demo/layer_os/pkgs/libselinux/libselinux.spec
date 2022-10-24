%global ruby_inc %(pkg-config --cflags ruby)
%global libsepol_version 3.3

Name:    libselinux
Version: 3.3
Release: 2
License: Public Domain
Summary: SELinux library and simple utilities
Url:     https://github.com/SELinuxProject/selinux/wiki
Source0: https://github.com/SELinuxProject/selinux/releases/download/3.3/libselinux-3.3.tar.gz

Patch6000: backport-libselinux-Close-leaked-FILEs.patch
Patch6001: backport-libselinux-free-memory-on-selabel_open-3-failure.patch
Patch6002: backport-libselinux-restorecon-misc-tweaks.patch
Patch6003: backport-libselinux-free-memory-in-error-branch.patch
Patch6004: backport-libselinux-restorecon-avoid-printing-NULL-pointer.patch

Patch9000: do-malloc-trim-after-load-policy.patch

BuildRequires: gcc python3-devel systemd swig pcre2-devel xz-devel
BuildRequires: ruby-devel libsepol-static

Requires:  libsepol >= %{libsepol_version} pcre2
Conflicts: filesystem < 3, selinux-policy-base < 3.13.1-138

Provides:  %{name}-utils = %{version}-%{release}
Obsoletes: %{name}-utils < %{version}-%{release}

%description
libselinux provides an interface to get and set process and file
security contexts and to obtain security policy decisions.

%package devel
Summary: Header files and libraries used to build SELinux
Requires: %{name} = %{version}-%{release}
Requires: libsepol-devel >= %{libsepol_version}

Provides:  %{name}-static = %{version}-%{release}
Obsoletes: %{name}-static < %{version}-%{release}

%description devel
libselinux provides an interface to get and set process and file
security contexts and to obtain security policy decisions.

%package -n python3-libselinux
Summary: SELinux python3 bindings for libselinux
Requires:  %{name} = %{version}-%{release}
Provides:  %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}

%description -n python3-libselinux
The libselinux-python3 package contains the python bindings for developing
SELinux applications.

%package ruby
Summary: SELinux ruby bindings for libselinux
Requires: %{name} = %{version}-%{release}
Provides: ruby(selinux)

%description ruby
The libselinux-ruby package contains the ruby bindings for developing
SELinux applications.

%package_help

%prep
%autosetup -p 1 -n libselinux-%{version}

%build
export LDFLAGS="%{?__global_ldflags}"
export DISABLE_RPM="y"
export USE_PCRE2="y"

make clean
%make_build LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" swigify
%make_build LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" all
%make_build %{__python3} LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" pywrap
%make_build RUBYINC="%{ruby_inc}" SHLIBDIR="%{_libdir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" CFLAGS="-g %{optflags}" rubywrap

%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sbindir}

install -d -m 0755 %{buildroot}%{_rundir}/setrans
echo "d %{_rundir}/setrans 0755 root root" > %{buildroot}%{_tmpfilesdir}/libselinux.conf

make PYTHON=%{__python3} DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" \
SHLIBDIR="%{_lib}" BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" LIBSEPOLA="%{_libdir}/libsepol.a" install-pywrap

make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" \
BINDIR="%{_bindir}" SBINDIR="%{_sbindir}" RUBYINSTALL=%{ruby_vendorarchdir} install install-rubywrap

rm -f %{buildroot}%{_sbindir}/{deftype,execcon,getenforcemode,getfilecon,getpidcon}
rm -f %{buildroot}%{_sbindir}/{mkdircon,policyvers,setfilecon,selinuxconfig,getseuser}
rm -f %{buildroot}%{_sbindir}/{compute_*,selinuxdisable,togglesebool,selinux_check_securetty_context}

mv %{buildroot}%{_sbindir}/getdefaultcon %{buildroot}%{_sbindir}/selinuxdefcon
mv %{buildroot}%{_sbindir}/getconlist %{buildroot}%{_sbindir}/selinuxconlist

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/libselinux.so.*
%{_sbindir}/{selabel_lookup_best_match,selabel_partial_match,selinux_check_access}
%{_sbindir}/{avcstat,getenforce,getsebool,matchpathcon,sefcontext_compile,selinuxconlist}
%{_sbindir}/{selinuxdefcon,selinuxexeccon,selinuxenabled,setenforce,selabel_digest,selabel_lookup}
%{_sbindir}/{selabel_get_digests_all_partial_matches,validatetrans}
%dir %{_rundir}/setrans/
%{_tmpfilesdir}/libselinux.conf

%files devel
%{_libdir}/libselinux.a
%{_libdir}/libselinux.so
%{_libdir}/pkgconfig/libselinux.pc
%{_includedir}/selinux/

%files -n python3-libselinux
%{python3_sitearch}/selinux/
%{python3_sitearch}/selinux-%{version}-*
%{python3_sitearch}/_selinux.*.so

%files ruby
%{ruby_vendorarchdir}/selinux.so

%files help
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/ru/man5/*
%{_mandir}/ru/man8/*

%changelog
* Sun Oct 9 2022 lujie <lujie54@huawei.com> - 3.3-2
- backport upstream patches

* Wed Dec 8 2021 lujie <lujie42@huawei.com> - 3.3-1
- update libselinux-3.1 to libselinux-3.3

* Tue Nov 16 2021 luhuaxin <1539327763@qq.com> - 3.1-5
- backport upstream patches

* Mon Nov 15 2021 lujie <lujie42@huawei.com> - 3.1-4
- fix potential undefined shifts

* Wed Jul 2 2021 luhuaxin <1539327763@qq.com> - 3.1-3
- do malloc trim after load policy

* Tue Oct 27 2020 gaoyusong <gaoyusong1@huawei.com> - 3.1-2
- delete BuildRequires python2-devel 

* Fri Jul 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.1-1
- update to 3.1; delete python2-libselinux

* Tue Jun 23 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.9-3
- add missing _selniux.so

* Mon Jun 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.9-2
- use python distutils to install selinux python bindings

* Thu Sep 5 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9-1
- Package init


