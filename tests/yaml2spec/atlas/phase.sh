#!/usr/bash

prep() {
%autosetup -n ATLAS -p1

cp %{SOURCE1} CONFIG/ARCHS/
cp %{SOURCE2} doc
cp %{SOURCE3} CONFIG/ARCHS/
cp %{SOURCE4} CONFIG/ARCHS/
cp %{SOURCE5} CONFIG/ARCHS/
cp %{SOURCE6} CONFIG/ARCHS/
cp %{SOURCE7} CONFIG/ARCHS/
cp %{SOURCE8} CONFIG/ARCHS/

mkdir lapacklib
cd lapacklib
ar x %{_libdir}/liblapack_pic.a
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
ar rcs ../liblapack_pic_pruned.a *.o
cd ..

}

build() {
p=$(pwd)
%undefine _strict_symbol_defs_build
%global mode -b %{__isa_bits}

%define arg_options %{nil}
%define flags %{nil}
%define threads_option "-t 2"

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

sed -i "s|SLAPACKlib.*|SLAPACKlib = ${p}/liblapack_pic_pruned.a|" Make.inc
cat Make.inc
make build
cd lib
make shared
make ptshared
popd
done

}

install() {
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

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/atlas.pc << EOF
Name: %{name}
Version: %{version}
Description: %{summary}
Cflags: -I%{_includedir}/atlas/
Libs: -L%{_libdir}/atlas/ -lsatlas
EOF

mkdir -p %{buildroot}%{_includedir}/atlas

}

check() {
for type in %{types}; do
pushd %{_arch}_${type}
make check ptcheck
popd
done

}
