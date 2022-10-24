Summary: Binary utilities
Name:    binutils
Version: 2.37
Release: 12
License: GPLv3+
URL:     https://sourceware.org/binutils

Source:  https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz

# risc-v do not support gold linker.
%ifnarch riscv64
%bcond_without gold
%else
%bcond_with gold
%endif

Patch0:  binutils-2.20.51.0.2-libtool-lib64.patch
Patch1:  export-demangle.h-in-devel-package.patch
#BUZ:845084
Patch2:  binutils-2.22.52.0.4-no-config-h-check.patch
#BUG:1452111
Patch3:  binutils-2.27-aarch64-ifunc.patch

#PATCH-CVE-UPSTREAM
Patch4:  CVE-2019-1010204.patch

Patch5:  Fix-a-potential-use-of-an-uninitialised-value-in-the.patch
Patch6:  backport-CVE-2021-45078.patch
Patch7:  backport-0001-CVE-2021-42574.patch
Patch8:  backport-0002-CVE-2021-42574.patch
Patch9:  backport-0003-CVE-2021-42574.patch
Patch10: bfd-Close-the-file-descriptor-if-there-is-no-archive.patch
Patch11: binutils-AArch64-EFI.patch
Patch12: backport-0001-PR28391-strip-objcopy-preserve-dates-.a-cannot-set-t.patch

Patch13: 0001-x86-Add-int1-as-one-byte-opcode-0xf1.patch
Patch14: 0002-x86-drop-OP_Mask.patch
Patch15: 0003-x86-correct-VCVT-U-SI2SD-rounding-mode-handling.patch
Patch16: 0004-x86-64-generalize-OP_G-s-EVEX.R-handling.patch
Patch17: 0005-x86-64-properly-bounds-check-bnd-N-in-OP_G.patch
Patch18: 0006-x86-fold-duplicate-register-printing-code.patch
Patch19: 0007-x86-fold-duplicate-code-in-MOVSXD_Fixup.patch
Patch20: 0008-x86-correct-EVEX.V-handling-outside-of-64-bit-mode.patch
Patch21: 0009-x86-drop-vex_mode-and-vex_scalar_mode.patch
Patch22: 0010-x86-fold-duplicate-vector-register-printing-code.patch
Patch23: 0011-x86-drop-xmm_m-b-w-d-q-_mode.patch
Patch24: 0012-x86-drop-vex_scalar_w_dq_mode.patch
Patch25: 0013-x86-drop-dq-b-d-_mode.patch
Patch26: 0014-x86-express-unduly-set-rounding-control-bits-in-disa.patch
Patch27: 0015-x86-Simplify-check-for-distinct-TMM-register-operand.patch
Patch28: 0016-PATCH-1-2-Enable-Intel-AVX512_FP16-instructions.patch
Patch29: 0017-PATCH-2-2-Add-tests-for-Intel-AVX512_FP16-instructio.patch
Patch30: 0018-x86-ELF-fix-.tfloat-output.patch
Patch31: 0019-x86-ELF-fix-.ds.x-output.patch
Patch32: 0020-x86-ELF-fix-.tfloat-output-with-hex-input.patch
Patch33: 0021-x86-introduce-.hfloat-directive.patch
Patch34: 0022-x86-Avoid-abort-on-invalid-broadcast.patch
Patch35: 0023-x86-Put-back-3-aborts-in-OP_E_memory.patch
Patch36: 0024-x86-Print-bad-on-invalid-broadcast-in-OP_E_memory.patch
Patch37: 0025-x86-Terminate-mnemonicendp-in-swap_operand.patch
Patch38: 0026-opcodes-Make-i386-dis.c-thread-safe.patch
Patch39: 0027-x86-reduce-AVX512-FP16-set-of-insns-decoded-through-.patch
Patch40: 0028-x86-reduce-AVX512-FP-set-of-insns-decoded-through-ve.patch
Patch41: 0029-x86-consistently-use-scalar_mode-for-AVX512-FP16-sca.patch
Patch42: backport-CVE-2022-38126.patch

Patch43: backport-0001-texi2pod.pl-add-no-op-no-split-option-support-PR2814.patch

Patch44: backport-AArch64-Add-support-for-AArch64-EFI-efi-aarch64.patch
Patch45: backport-Add-support-for-AArch64-EFI-efi-aarch64.patch
Patch46: backport-don-t-over-align-file-positions-of-PE-executable-sec.patch

Provides: bundled(libiberty)

Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: gcc, perl, sed, coreutils, dejagnu, zlib-devel, glibc-static, sharutils, bc, libstdc++-static
BuildRequires: bison, m4, gcc-c++, gettext, flex, zlib-devel, texinfo >= 4.0, perl-podlators chrpath
Requires(post): info coreutils chkconfig
Requires(preun):info chkconfig

%define _gnu %{nil}
# The higher of these two numbers determines the default ld.
%{!?ld_bfd_priority: %global ld_bfd_priority    50}

%if %{with gold}
%{!?ld_gold_priority:%global ld_gold_priority   30}
%endif

%description
The GNU Binutils are a collection of binary tools. The main ones are:
ld - the GNU linker.
as - the GNU assembler.
addr2line - Converts addresses into filenames and line numbers.
ar - A utility for creating, modifying and extracting from archives.
c++filt - Filter to demangle encoded C++ symbols.
dlltool - Creates files for building and using DLLs.
gold - A new, faster, ELF only linker, still in beta test.
gprof - Displays profiling information.
nlmconv - Converts object code into an NLM.
nm - Lists symbols from object files.
objcopy - Copies and translates object files.
objdump - Displays information from object files.
ranlib - Generates an index to the contents of an archive.
readelf - Displays information from any ELF format object file.
size - Lists the section sizes of an object or archive file.
strings - Lists printable strings from files.
trip - Discards symbols.
windmc - A Windows compatible message compiler.
windres - A compiler for Windows resource files.


%package devel
Summary: devel package including header files and libraries.
Provides: binutils-static = %{version}-%{release}
Requires: zlib-devel, binutils = %{version}-%{release}, coreutils
Requires(post): info
Requires(preun):info

%description devel
The devel package contains BFD and opcodes static and dynamic libraries.
The static libraries are used by the dynamic libraries which are linkier
scripts imported from glibc/Makerules.

%package help
Summary: binutils help

%description help
The help package contains man files.

%prep
%autosetup -n %{name}-%{version} -p1


sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*

sed -i -e '/pagesize/s/0x1000,/0x10000,/' gold/aarch64.cc
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*aarch64.c

sed -i -e 's/^ PACKAGE=/ PACKAGE=/' */configure
# revert name change when testing.
sed -i -e "2aDEJATOOL = binutils" binutils/Makefile.am
sed -i -e "2aDEJATOOL = gas" gas/Makefile.am
sed -i -e "2aDEJATOOL = ld" ld/Makefile.am
sed -i -e "s/^DEJATOOL = .*/DEJATOOL = binutils/" binutils/Makefile.in
sed -i -e "s/^DEJATOOL = .*/DEJATOOL = gas/" gas/Makefile.in
sed -i -e "s/^DEJATOOL = .*/DEJATOOL = ld/" ld/Makefile.in

touch gas/doc/as.texi
touch */configure

%build
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

%configure \
  --quiet \
  --build=%{_target_platform} --host=%{_target_platform} \
  --target=%{_target_platform} \
  --enable-ld \
%if %{with gold}
  --enable-gold=default \
%endif
  --with-sysroot=/ \
  --enable-deterministic-archives=no \
  --enable-lto \
  --enable-compressed-debug-sections=none \
  --enable-generate-build-notes=no \
  $CARGS \
  --enable-plugins \
  --enable-shared

%make_build %{_smp_mflags} tooldir=%{_prefix} all
%make_build %{_smp_mflags} tooldir=%{_prefix} info

%check
make -k check < /dev/null || :
cat {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
do
  ln $file binutils-%{_target_platform}-$(basename $file) || :
done
tar cjf binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
uuencode binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}.tar.bz2
rm -f binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}

%install
%make_install DESTDIR=%{buildroot}

make prefix=%{buildroot}%{_prefix} infodir=%{buildroot}%{_infodir} install-info

for library in bfd/libbfd.a libiberty/libiberty.a opcodes/libopcodes.a
do
  install -m 644 $library %{buildroot}%{_libdir}
done

install -m 644 include/libiberty.h %{buildroot}%{_prefix}/include
chmod +x %{buildroot}%{_libdir}/lib*.so*

rm -f %{buildroot}%{_libdir}/lib{bfd,opcodes}.{so,la}

#Remove rpath
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

# Generate libbfd.so and libopcodes.so

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

%post
%__rm -f %{_bindir}/ld
%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/ld.bfd %{ld_bfd_priority}

%if %{with gold}
%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/ld.gold %{ld_gold_priority}
%endif

if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --auto ld
fi

/sbin/ldconfig

%post help
for info in as.info.gz binutils.info.gz gprof.info.gz ld.info.gz
do
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/$info
done

%preun
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove ld %{_bindir}/ld.bfd

%if %{with gold}  
  %{_sbindir}/alternatives --remove ld %{_bindir}/ld.gold
%endif
fi

%preun help
if [ $1 = 0 ]; then
  if [ -e %{_infodir}/binutils.info.gz ]
  then
    for info in as.info.gz binutils.info.gz gprof.info.gz ld.info.gz
    do
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/$info
    done
  fi
fi


%postun
/sbin/ldconfig

%postun help
  if [ -e %{_infodir}/binutils.info.gz ]
  then
    for info in as.info.gz binutils.info.gz gprof.info.gz ld.info.gz
    do
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/$info
    done
  fi


%files -f binutils.lang
%doc README
%license COPYING3 COPYING COPYING3.LIB COPYING.LIB
%{_bindir}/[!l]*
%{_bindir}/ld.*
%ghost %{_bindir}/ld
%{_libdir}/lib*.so
%{_libdir}/libctf*
%{_libdir}/bfd-plugins/libdep.so
%exclude %{_libdir}/libctf.a
%exclude %{_libdir}/libctf-nobfd.a
%exclude %{_libdir}/libbfd.so
%exclude %{_libdir}/libopcodes.so
%config(noreplace) /etc/ld.so.conf.d/*

%files devel
%{_prefix}/include/*
%{_libdir}/lib*.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.so

%files help
%{_mandir}/man1/*
%{_infodir}/as.info.gz
%{_infodir}/binutils.info.gz
%{_infodir}/gprof.info.gz
%{_infodir}/ld.info.gz
%{_infodir}/[^b]*info*
%{_infodir}/binutils*info*
%{_infodir}/bfd*info*

%changelog
* Sat Oct 08 2022 Chenxi Mao <chenxi.mao@suse.com> - 2.37-12
- Fix Aarch64 EFI PE section address overlap issue.

* Fri Sep 02 2022 Wei, Qiang <qiang.wei@suse.com> - 2.37-11
- Fix man page empty issue

* Thu Sep 8 2022 yinyongkang <yinyongkang@kylinos.cn> - 2.37-10
- Type:CVE
- ID:CVE-2022-38126
- SUG:NA
- DESC:Fix CVE-2022-38126

* Tue Aug 11 2022 dingguangya <dingguangya1@huawei.com> - 2.37-9
- Type:requirements
- ID:NA
- SUG:NA
- DESC:Enable Intel AVX512_FP16 instructions

* Fri Aug 05 2022 maminjie <maminjie8@163.com> - 2.37-8
- Fix preserve_dates: cannot set time

* Wed Jun 29 2022 Chenxi Mao <chenxi.mao@suse.com> - 2.37-7
- Add support for the EFI format to the AArch64 target.

* Tue Mar 15 2022 zoulin <zoulin13@h-partners.com> - 2.37-6
- Type:requirements
- ID:NA
- SUG:NA
- DESC:fix (obs) project build fail

* Sat Mar 12 2022 zoulin <zoulin13@h-partners.com> - 2.37-5
- Type:requirements
- ID:NA
- SUG:NA
- DESC:add binutils-extra

* Fri Jan 21 2022 Kai Liu <kai.liu@suse.com> - 2.37-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix upstream bug #28138, which results in "malformed archive" error when building nodejs

* Wed Jan 19 2022 panxiaohe <panxiaohe@huawei.com> - 2.37-3
- Type:CVE
- ID:CVE-2021-42574
- SUG:NA
- DESC:Fix CVE-2021-42574

* Fri Dec 24 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.37-2
- Type:CVE
- ID:CVE-2021-45078
- SUG:NA
- DESC:Fix CVE-2021-45078

* Thu Dec 2 2021 wangchen <wangchen137@huawei.com> - 2.37-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC:update to 2.37

* Tue Sep 14 2021 panxiaohe <panxiaohe@huawei.com> - 2.36.1-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: fix issue about delete symlink when using the strip command

* Tue Sep 7 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.36.1-2
- Type:requirements
- ID:NA
- SUG:NA
- DESC:remove rpath and runpath of exec files and libraries

* Mon Jul 5 2021 yixiangzhike <zhangxingliang3@huawei.com> - 2.36.1-1
- Type:NA
- ID:NA
- SUG:NA
- DESC: update to 2.36.1

* Sat Jun 19 2021 wangchen <wangchen137@huawei.com> - 2.34-13
- Type:CVE
- ID:NA
- SUG:NA
- DESC: fix CVE-2021-3549

* Fri Apr 23 2021 lirui <lirui130@huawei.com> - 2.34-12
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2021-3487

* Fri Apr 16 2021 lirui <lirui130@huawei.com> - 2.34-11
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2021-20197

* Tue Mar 23 2021 panxiaohe <panxiaohe@huawei.com> - 2.34-10
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2020-0551

* Mon Mar 22 2021 lirui <lirui130@huawei.com> - 2.34-9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:move the test to %check phase

* Sat Jan 9 2021 zoulin <zoulin13@huawei.com> - 2.34-8
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2020-16592

* Wed Nov 4 2020 Qingqing Li <liqingqing3@huawei.com> - 2.34-7
- Type:bugfix
- ID:NA
- SUG:fully support for riscv64.

* Tue Nov 3 2020 Qingqing Li <liqingqing3@huawei.com> - 2.34-6
- Type:bugfix
- ID:NA
- SUG:riscv64 do not support gold linker, add a condition to distinguish it.

* Sat Oct 31 2020 Qingqing Li <liqingqing3@huawei.com> - 2.34-5
- Type:bugfix
- ID:NA
- SUG:fix changelog date.

* Fri Sep 18 2020 zoulin <zoulin13@huawei.com> - 2.34-4
- Type:bugfix
- ID:NA
- SUG:Fix a potential use-of-an-uninitialised-value in the print_insn_ns32k of fuzz_disassemble

* Fri Sep 11 2020 zoulin <zoulin13@huawei.com> - 2.34-3
- Type:bugfix
- ID:NA
- SUG:Fix a memory leak in the testcase fuzz_readelf
      Fix use-of-uninitialized-value in print_insn_mwtag
      Fix use-of-ninitialized-value in _bfd_xcoff_slurp_armap

* Wed Aug 5 2020 zhangxingliang <zhangxingliang3@huawei.com> - 2.34-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix static library file conflicts when install both binutils and binutils-devel

* Fri Jul 24 2020 zhangxingliang <zhangxingliang3@huawei.com> - 2.34-1
- Type:update
- ID:NA
- SUG:NA
- DESC:update to 2.34

* Tue Jul 14 2020 linwei <linwei54@huawei.com> - 2.33.1-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix use-of-uninitialized-value in print_insn_nds32

* Fri May 15 2020 wangchen <wangchen137@huawei.com> - 2.33.1-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix memory leak in bfd_check_format

* Thu Apr 02 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Use disassemble_info.private_date in place of insn_sets 

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-5
- Type:bugfix
- ID:CVE
- SUG:NA
- DESC: fix permission

* Mon Jan 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-4
- Type:bugfix
- ID:CVE
- SUG:NA
- DESC:fix the issue that the permission changes due to the upgrade and
       backport patch to fix memory leak and overflow

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-3
- Type:bugfix
- ID:CVE
- SUG:NA
- DESC:add patch to solve complaining about relocs in the .gnu.build.attribute

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-2
- Type:bugfix
- ID:CVE
- SUG:NA
- DESC:add libbfd.so and libopcodes.so for kernel building

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-1
- Type:enhancement
- ID:CVE
- SUG:NA
- DESC:update version to 2.33.1

* Fri Dec 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.31.1-16
- Type:cves
- ID:CVE
- SUG:NA
- DESC:fix CVE-2018-20671 CVE-2019-12972 CVE-2019-17450 CVE-2019-17451
       CVE-2018-18309 CVE-2018-18309 CVE-2018-18605 CVE-2018-18607 CVE-2018-18606
       CVE-2018-1000876 CVE-2018-20002 CVE-2018-20002 CVE-2019-1010180
       fix failure in the libiberty testsuite
       fix stack-buffer-overflow, and use-of-uninitialized-value and shift exponent -1 is negative

* Mon Sep 23 2019 luhuaxin <luhuaxin@huawei.com> - 2.31.1-15
- Patch synchronization and update dependency name
- Type:cves
- ID:CVE-2019-1010204
- SUG:NA
- DESC:fix CVE-2019-1010204

* Wed Sep 04 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.31.1-14
- Package init
