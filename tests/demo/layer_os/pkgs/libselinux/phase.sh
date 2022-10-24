#!/usr/bash

prep() {
%autosetup -p 1 -n libselinux-%{version}

}

build() {
export LDFLAGS="%{?__global_ldflags}"
export DISABLE_RPM="y"
export USE_PCRE2="y"

make clean
%make_build LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" swigify
%make_build LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" all
%make_build %{__python3} LIBDIR="%{_libdir}" CFLAGS="-g %{optflags}" pywrap
%make_build RUBYINC="%{ruby_inc}" SHLIBDIR="%{_libdir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" CFLAGS="-g %{optflags}" rubywrap

}

install() {
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

}

