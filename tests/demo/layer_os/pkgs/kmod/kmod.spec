Name:           kmod
Version:        30
Release:        2
Summary:        Kernel module management
# GPLv2+ is used by programs, LGPLv2+ is used for libraries.
License:        GPLv2+ and LGPLv2+
URL:            http://git.kernel.org/?p=utils/kernel/kmod/kmod.git;a=summary
Source0:        https://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
Source1:        weak-modules
Source2:        depmod.conf.dist

BuildRequires:  gcc chrpath zlib-devel xz-devel libxslt openssl-devel

Provides:       module-init-tools = 4.0-1
Provides:       /sbin/modprobe
Patch:		0001-Module-replace-the-module-with-new-module.patch
Patch:		0002-Module-suspend-the-module-by-rmmod-r-option.patch

%description
The kmod package provides several commands to manage the kernel modules,
such as insmod to load and rmmod to unload the modules.

%package libs
Summary:    Libraries to handle kernel module loading and unloading
License:    LGPLv2+

%description libs
The kmod-libs package provides runtime libraries for any application that
wishes to load or unload Linux kernel modules from the running system.

%package devel
Summary:        Header files for kmod development
Requires:       %{name} = %{version}-%{release} %{name}-libs

%description devel
The kmod-devel package provides header files used for loading or unloading
kernel modules.

%package -n python3-kmod
Summary:       Python3 bindings for kmod/libkmod.
BuildRequires: python3 python3-devel python3-Cython kmod-devel kmod-libs
Requires:      python3

%description -n python3-kmod
python3-kmod is a Python3 wrapper module for libkmod, exposing common
module operations: listing installed modules, modprobe, and rmmod.

%package help
Summary:        Documents and man pages for the kmod
Requires:       man info

%description help
The kmod-help package provides several documents and the man pages to help
developers to understand the kmod.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --with-openssl --with-zlib --with-xz --enable-python
%make_build

%install
%make_install
rm -f %{buildroot}%{python3_sitearch}/kmod/*.la
pushd $RPM_BUILD_ROOT/%{_mandir}/man5
ln -s modprobe.d.5.gz modprobe.conf.5.gz
popd

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
for i in $RPM_BUILD_ROOT%{_sbindir}/modprobe $RPM_BUILD_ROOT%{_sbindir}/modinfo $RPM_BUILD_ROOT%{_sbindir}/insmod \
         $RPM_BUILD_ROOT%{_sbindir}/rmmod $RPM_BUILD_ROOT%{_sbindir}/depmod $RPM_BUILD_ROOT%{_sbindir}/lsmod
do
    ln -sf ../bin/kmod $i
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d
mkdir -p $RPM_BUILD_ROOT/sbin

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/weak-modules
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d/dist.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%exclude %{_libdir}/*.la

%dir %{_sysconfdir}/*.d
%dir %{_prefix}/lib/modprobe.d

%{_bindir}/kmod
%{_sbindir}/*
%{_datadir}/bash-completion/
%{_sysconfdir}/depmod.d/dist.conf

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libkmod.so.*

%files devel
%{_includedir}/libkmod.h
%{_libdir}/pkgconfig/libkmod.pc
%{_libdir}/libkmod.so

%files -n python3-kmod
%{python3_sitearch}/kmod/

%files help
%attr(0644,root,root) %{_mandir}/man5/*.5*
%attr(0644,root,root) %{_mandir}/man8/*.8*

%doc TODO NEWS README.md

%changelog
