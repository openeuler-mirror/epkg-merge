#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1


sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*

sed -i -e '/pagesize/s/0x1000,/0x10000,/' gold/aarch64.cc
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*aarch64.c

sed -i -e 's/^ PACKAGE=/ PACKAGE=/' */configure
sed -i -e "2aDEJATOOL = binutils" binutils/Makefile.am
sed -i -e "2aDEJATOOL = gas" gas/Makefile.am
sed -i -e "2aDEJATOOL = ld" ld/Makefile.am
sed -i -e "s/^DEJATOOL = .*/DEJATOOL = binutils/" binutils/Makefile.in
sed -i -e "s/^DEJATOOL = .*/DEJATOOL = gas/" gas/Makefile.in
sed -i -e "s/^DEJATOOL = .*/DEJATOOL = ld/" ld/Makefile.in

touch gas/doc/as.texi
touch */configure

}

build() {
CARGS=
case %{_target_platform} in i?86*|arm*|aarch64*|riscv64*)
CARGS="$CARGS --enable-64-bit-bfd"
;;
esac

case %{_target_platform} in x86_64*|i?86*|aarch64*|riscv64*)
CARGS="$CARGS --enable-targets=x86_64-pep --enable-relro=yes"
;;
esac

export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS=$RPM_LD_FLAGS

%configure %%{env.configureFlags} $CARGS \
  --quiet \
  --build=%{_target_platform} --host=%{_target_platform} \
  --target=%{_target_platform} \
%if %{with gold}
--enable-gold=default \
%endif

%make_build %{_smp_mflags} tooldir=%{_prefix} all
%make_build %{_smp_mflags} tooldir=%{_prefix} info

}

check() {
make -k check < /dev/null || :
cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
do
ln $file binutils-%{_target_platform}-$(basename $file) || :
done
tar cjf binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
uuencode binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}.tar.bz2
rm -f binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}

}

install() {
%make_install DESTDIR=%{buildroot}

make prefix=%{buildroot}%{_prefix} infodir=%{buildroot}%{_infodir} install-info

for library in bfd/libbfd.a libiberty/libiberty.a opcodes/libopcodes.a
do
install -m 644 $library %{buildroot}%{_libdir}
done

install -m 644 include/libiberty.h %{buildroot}%{_prefix}/include
chmod +x %{buildroot}%{_libdir}/lib*.so*

rm -f %{buildroot}%{_libdir}/lib{bfd,opcodes}.{so,la}

chrpath --delete %{buildroot}%{_bindir}/{ld.bfd,objcopy,addr2line,gprof,size,strings,c++filt,strip,as,objdump,nm,ranlib,ar,readelf}
chrpath --delete %{buildroot}%{_libdir}/libopcodes-%{version}.so
chrpath --delete %{buildroot}%{_libdir}/libctf.so.0.0.0

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%ifarch %{ix86} x86_64 arm
sed -i -e '/^#include "ansidecl.h"/{p;s~^.*$~#include <bits/wordsize.h>~;}' \
    -e 's/^#define BFD_DEFAULT_TARGET_SIZE \(32\|64\) *$/#define BFD_DEFAULT_TARGET_SIZE __WORDSIZE/' \
    -e 's/^#define BFD_HOST_64BIT_LONG [01] *$/#define BFD_HOST_64BIT_LONG (__WORDSIZE == 64)/' \
    -e 's/^#define BFD_HOST_64_BIT \(long \)\?long *$/#if __WORDSIZE == 32\
#define BFD_HOST_64_BIT long long\
#else\
#define BFD_HOST_64_BIT long\
#endif/' \
    -e 's/^#define BFD_HOST_U_64_BIT unsigned \(long \)\?long *$/#define BFD_HOST_U_64_BIT unsigned BFD_HOST_64_BIT/' \
    %{buildroot}%{_prefix}/include/bfd.h
%endif
touch -r bfd/bfd-in2.h %{buildroot}%{_prefix}/include/bfd.h


%ifarch x86_64
tee %{buildroot}%{_libdir}/libbfd.so <<EOF
/* GNU ld script */

OUTPUT_FORMAT(elf64-x86-64)

INPUT ( %{_libdir}/libbfd.a -liberty -lz -ldl )
EOF

tee %{buildroot}%{_libdir}/libopcodes.so <<EOF
/* GNU ld script */

OUTPUT_FORMAT(elf64-x86-64)

INPUT ( %{_libdir}/libopcodes.a -lbfd )
EOF
%endif

%ifarch aarch64
tee %{buildroot}%{_libdir}/libbfd.so <<EOF
/* GNU ld script */

OUTPUT_FORMAT(elf64-littleaarch64)

INPUT ( %{_libdir}/libbfd.a -liberty -lz -ldl )
EOF

tee %{buildroot}%{_libdir}/libopcodes.so <<EOF
/* GNU ld script */

OUTPUT_FORMAT(elf64-littleaarch64)

INPUT ( %{_libdir}/libopcodes.a -lbfd )
EOF
%endif

%ifarch riscv64
tee %{buildroot}%{_libdir}/libbfd.so <<EOF
/* GNU ld script */

OUTPUT_FORMAT(elf64-littleriscv)

INPUT ( %{_libdir}/libbfd.a -liberty -lz -ldl )
EOF

tee %{buildroot}%{_libdir}/libopcodes.so <<EOF
/* GNU ld script */

OUTPUT_FORMAT(elf64-littleriscv)

INPUT ( %{_libdir}/libopcodes.a -lbfd )
EOF
%endif

rm -f %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_prefix}/%{_target_platform}

%find_lang binutils
%if %{with gold}
for library in opcodes bfd gas gprof ld gold
%else
for library in opcodes bfd gas gprof ld
%endif
do
%find_lang $library
cat $library.lang >> binutils.lang
done

}

