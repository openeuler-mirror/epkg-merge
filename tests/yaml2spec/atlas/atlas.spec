#Global macro or variable
%global _hardened_build 1
%define types base

#Basic Information
Name:           atlas
Version:        3.10.3
Release:        11
Summary:        Automatically Tuned Linear Algebra Software
License:        BSD
URL:            http://math-atlas.sourceforge.net/
Source0:        http://downloads.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
Source1:        PPRO32.tgz
Source2:        README.dist
Source3:        POWER332.tar.bz2
Source4:        IBMz932.tar.bz2
Source5:        IBMz964.tar.bz2
Source6:        ARMv732NEON.tar.bz2
Source7:        IBMz1264.tar.bz2
Source8:        ARMa732.tar.bz2
Patch0000:      atlas-melf.patch
Patch0001:      atlas-shared_libraries.patch
Patch0002:      atlas-genparse.patch
Patch0003:      atlas.3.10.1-unbundle.patch
Patch0004:      0001-sed-tune-macro-value-to-repair-binary-diffence.patch
Patch0005:      atl-date-to-eliminate-difference.patch
Patch0006:      ret-iaff-to-eliminate-difference.patch
Patch0007:      mv-res-taffinity.patch
Patch0008:      atlas-compatible-with-hcc.patch
Patch0009:      0001-fix-gcc-version-check.patch
Patch0010:	atlas-riscv64-port.patch

#Dependency
BuildRequires:  gcc-gfortran, lapack-devel, gcc

%ifarch x86_64
Obsoletes:      atlas-sse3 < 3.10.3-1
%endif

%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK

%package devel
Summary:                Development libraries for ATLAS
Requires:               %{name} = %{version}-%{release}
Obsoletes:              %{name}-header <= %{version}-%{release}
Requires(posttrans):    chkconfig
Requires(postun):       chkconfig

Provides:               %{name}-static = %{version}-%{release}
Obsoletes:              %{name}-static < %{version}-%{release}

%ifarch x86_64
Obsoletes:              atlas-sse3-devel < 3.10.3-1
Obsoletes:              atlas-sse3-static < 3.10.3-1
%endif

%description devel
This package contains headers and static librariesfor development with
ATLAS (Automatically Tuned Linear Algebra Software).

#Secondary package
%ifarch x86_64
%define types base corei2
%package corei2
Summary:    ATLAS libraries for Corei2 (Ivy/Sandy bridge) CPUs

%description corei2
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the Corei2 (Ivy/Sandy bridge)
CPUs.
The base ATLAS builds for the x86_64 architecture are made for the hammer64 CPUs.

%package corei2-devel
Summary:        ATLAS development libraries for ATLAS for Corei2 (Ivy/Sandy bridge) CPUs
Requires:       %{name}-corei2 = %{version}-%{release}
Obsoletes:      %{name}-header <= %{version}-%{release}
Requires(posttrans):    chkconfig
Requires(postun):       chkconfig

Provides:       %{name}-corei2-static = %{version}-%{release}
Obsoletes:      %{name}-corei2-static < %{version}-%{release}

%description corei2-devel
This package contains shared and static versions of the ATLAS libraries compiled with
optimizations for the corei2 (Ivy/Sandy bridge) CPUs.
The base ATLAS builds for the x86_64 architecture are made for the hammer64 CPUs.
%endif

#Build sections
%prep
%autosetup -n ATLAS -p1

cp %{SOURCE1} CONFIG/ARCHS/
cp %{SOURCE2} doc
cp %{SOURCE3} CONFIG/ARCHS/
cp %{SOURCE4} CONFIG/ARCHS/
cp %{SOURCE5} CONFIG/ARCHS/
cp %{SOURCE6} CONFIG/ARCHS/
cp %{SOURCE7} CONFIG/ARCHS/
cp %{SOURCE8} CONFIG/ARCHS/

# Generate lapack library
mkdir lapacklib
cd lapacklib
ar x %{_libdir}/liblapack_pic.a
# Remove functions that have ATLAS implementations
rm -f cgelqf.o cgels.o cgeqlf.o cgeqrf.o cgerqf.o cgesv.o cgetrf.o cgetri.o \
      cgetrs.o clarfb.o clarft.o clauum.o cposv.o cpotrf.o cpotri.o cpotrs.o \
      ctrtri.o dgelqf.o dgels.o dgeqlf.o dgeqrf.o dgerqf.o dgesv.o dgetrf.o \
      dgetri.o dgetrs.o dlamch.o dlarfb.o dlarft.o dlauum.o dposv.o dpotrf.o \
      dpotri.o dpotrs.o dtrtri.o ieeeck.o ilaenv.o lsame.o sgelqf.o sgels.o \
      sgeqlf.o sgeqrf.o sgerqf.o sgesv.o sgetrf.o sgetri.o sgetrs.o slamch.o \
      slarfb.o slarft.o slauum.o sposv.o spotrf.o spotri.o spotrs.o strtri.o \
      xerbla.o zgelqf.o zgels.o zgeqlf.o zgeqrf.o zgerqf.o zgesv.o zgetrf.o \
      zgetri.o zgetrs.o zlarfb.o zlarft.o zlauum.o zposv.o zpotrf.o zpotri.o \
      zpotrs.o ztrtri.o
# Create new library
ar rcs ../liblapack_pic_pruned.a *.o
cd ..

%build
p=$(pwd)
%undefine _strict_symbol_defs_build
%global mode -b %{__isa_bits}

%define arg_options %{nil}
%define flags %{nil}
%define threads_option "-t 2"

#Target architectures for the 'base' versions
%ifarch x86_64
%define flags %{nil}
%define base_options "-A HAMMER -V 896"
%endif

%ifarch aarch64
%define flags %{nil}
%define base_options "-A ARM64a53 -V 1"
%endif

%ifarch riscv64
%define flags %{nil}
%define base_options "-A RISCV64 -V 1"
%endif

for type in %{types}; do
    if [ "$type" = "base" ]; then
        libname=atlas
        arg_options=%{base_options}
        thread_options=%{threads_option}
        %define pr_base %(echo $((%{__isa_bits}+0)))
    else
        libname=atlas-${type}
        if [ "$type" = "corei2" ]; then
            thread_options="-t 4"
            arg_options="-A Corei2 -V 896"
            %define pr_corei2 %(echo $((%{__isa_bits}+2)))
        fi
    fi
    mkdir -p %{_arch}_${type}
    pushd %{_arch}_${type}
    ../configure  %{mode} $thread_options $arg_options -D c -DWALL -Fa alg '%{flags} -g -Wa,--noexecstack -fPIC ${RPM_LD_FLAGS} -fstack-protector-all -Wl,-z,now'\
    --prefix=%{buildroot}%{_prefix}            \
    --incdir=%{buildroot}%{_includedir}        \
    --libdir=%{buildroot}%{_libdir}/${libname}

    #matches both SLAPACK and SSLAPACK
    sed -i "s|SLAPACKlib.*|SLAPACKlib = ${p}/liblapack_pic_pruned.a|" Make.inc
    cat Make.inc
    make build
    cd lib
    make shared
    make ptshared
    popd
done

%install
for type in %{types}; do
    pushd %{_arch}_${type}
    make DESTDIR=%{buildroot} install
        mv %{buildroot}%{_includedir}/atlas %{buildroot}%{_includedir}/atlas-%{_arch}-${type}
    if [ "$type" = "base" ]; then
        cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas/
        rm -f %{buildroot}%{_libdir}/atlas/*.a
        cp -pr lib/libcblas.a lib/libatlas.a lib/libf77blas.a lib/liblapack.a %{buildroot}%{_libdir}/atlas/
    else
        cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas-${type}/
        rm -f %{buildroot}%{_libdir}/atlas-${type}/*.a
        cp -pr lib/libcblas.a lib/libatlas.a lib/libf77blas.a lib/liblapack.a %{buildroot}%{_libdir}/atlas-${type}/
    fi
    popd

    mkdir -p %{buildroot}/etc/ld.so.conf.d
    if [ "$type" = "base" ]; then
        echo "%{_libdir}/atlas"        \
        > %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}.conf
    else
        echo "%{_libdir}/atlas-${type}"    \
        > %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}-${type}.conf
    fi
done

#create pkgconfig file
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/atlas.pc << EOF
Name: %{name}
Version: %{version}
Description: %{summary}
Cflags: -I%{_includedir}/atlas/
Libs: -L%{_libdir}/atlas/ -lsatlas
EOF

mkdir -p %{buildroot}%{_includedir}/atlas

%check
for type in %{types}; do
    pushd %{_arch}_${type}
    make check ptcheck
    popd
done

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%posttrans devel
/usr/sbin/alternatives --install %{_includedir}/atlas atlas-inc \
        %{_includedir}/atlas-%{_arch}-base %{pr_base}

%postun devel
if [ $1 -ge 0 ] ; then
    /usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-base
fi

%if "%{?enable_native_atlas}" == "0"

%ifarch x86_64
%post -n atlas-corei2 -p /sbin/ldconfig

%postun -n atlas-corei2 -p /sbin/ldconfig

%posttrans corei2-devel
    /usr/sbin/alternatives --install %{_includedir}/atlas atlas-inc     \
        %{_includedir}/atlas-%{_arch}-corei2  %{pr_corei2}

%postun corei2-devel
if [ $1 -ge 0 ] ; then
    /usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-corei2
fi
%endif

%endif


%files
%doc doc/README.dist
%dir %{_libdir}/atlas
%{_libdir}/atlas/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}.conf

%files devel
%doc doc
%{_libdir}/atlas/*.so
%{_libdir}/atlas/*.a
%{_includedir}/atlas-%{_arch}-base/
%{_includedir}/*.h
%ghost %{_includedir}/atlas
%{_libdir}/pkgconfig/atlas.pc

%ifarch x86_64
%files corei2
%doc doc/README.dist
%dir %{_libdir}/atlas-corei2
%{_libdir}/atlas-corei2/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-corei2.conf

%files corei2-devel
%doc doc
%{_libdir}/atlas-corei2/*.so
%{_libdir}/atlas-corei2/*.a
%{_includedir}/atlas-%{_arch}-corei2/
%{_includedir}/*.h
%ghost %{_includedir}/atlas
%endif

%changelog
* Fri Nov 13 2020 yangyanchao <yangyanchao6@huawei.com> - 3.10.3-11
- Add a machine type to Support riscv

* Mon Sep 14 2020 lingsheng <lingsheng@huawei.com> - 3.10.3-10
- Fix gcc version check

* Wed Mar 18 2020 lihao <lihao129@huawei.com> - 3.10.3-9
- Enable BIND_NOW and stack protector

* Fri Nov 15 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.10.3-8
- package init

