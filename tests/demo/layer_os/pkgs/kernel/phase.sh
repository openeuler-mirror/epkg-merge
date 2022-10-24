#!/usr/bash

prep() {

%setup -q -n kernel-%{version} -c

%if 0%{?with_patch}
tar -xjf %{SOURCE13}
%endif

mv kernel linux-%{KernelVer}
cd linux-%{KernelVer}

cp %{SOURCE4} certs

%if 0%{?with_patch}
cp %{SOURCE10} .
cp %{SOURCE11} .
cp %{SOURCE12} .

if [ ! -d patches ];then
mv ../patches .
fi

Applypatches()
{
set -e
set -o pipefail
local SERIESCONF=$1
local PATCH_DIR=$2
sed -i '/^#/d'  $SERIESCONF
sed -i '/^[\s]*$/d' $SERIESCONF
(
echo "trap 'echo \"*** patch \$_ failed ***\"' ERR"
echo "set -ex"
cat $SERIESCONF | \
        sed "s!^!patch -s -F0 -E -p1 --no-backup-if-mismatch -i $PATCH_DIR/!" \
    ) | sh
}

Applypatches series.conf %{_builddir}/kernel-%{version}/linux-%{KernelVer}
%endif

touch .scmversion

find . \( -name "*.orig" -o -name "*~" \) -exec rm -f {} \; >/dev/null
find . -name .gitignore -exec rm -f {} \; >/dev/null

%if 0%{?with_signmodules}
cp %{SOURCE2} certs/.
%endif

pathfix.py -pni "/usr/bin/python" tools/power/pm-graph/sleepgraph.py tools/power/pm-graph/bootgraph.py tools/perf/scripts/python/exported-sql-viewer.py

%if 0%{?with_source}
# Copy directory backup for kernel-source
cp -a ../linux-%{KernelVer} ../linux-%{KernelVer}-source
find ../linux-%{KernelVer}-source -type f -name "\.*" -exec rm -rf {} \; >/dev/null
%endif

cp -a tools/perf tools/python3-perf

}

build() {
cd linux-%{KernelVer}

perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}.%{_target_cpu}/" Makefile

make mrproper %{_smp_mflags}

%if %{with_64kb}
sed -i arch/arm64/configs/openeuler_defconfig -e 's/^CONFIG_ARM64_4K_PAGES.*/CONFIG_ARM64_64K_PAGES=y/'
sed -i arch/arm64/configs/openeuler_defconfig -e 's/^CONFIG_ARM64_PA_BITS=.*/CONFIG_ARM64_PA_BITS=52/'
sed -i arch/arm64/configs/openeuler_defconfig -e 's/^CONFIG_ARM64_PA_BITS_.*/CONFIG_ARM64_PA_BITS_52=y/'
sed -i arch/arm64/configs/openeuler_defconfig -e 's/^CONFIG_ARM64_VA_BITS=.*/CONFIG_ARM64_VA_BITS=52/'
sed -i arch/arm64/configs/openeuler_defconfig -e 's/^CONFIG_ARM64_VA_BITS_.*/CONFIG_ARM64_VA_BITS_52=y/'
%endif

make ARCH=%{Arch} openeuler_defconfig

TargetImage=$(basename $(make -s image_name))

make ARCH=%{Arch} $TargetImage %{?_smp_mflags}
make ARCH=%{Arch} modules %{?_smp_mflags}

%if 0%{?with_kabichk}
chmod 0755 %{SOURCE5}
if [ -e $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu} ]; then
##%{SOURCE5} -k $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu} -s Module.symvers || exit 1
echo "**** NOTE: now don't check Kabi. ****"
else
echo "**** NOTE: Cannot find reference Module.kabi file. ****"
fi
%endif

%ifarch aarch64
make ARCH=%{Arch} dtbs
%endif

%if %{with_perf}
# perf
%global perf_make \
    make EXTRA_CFLAGS="-Wl,-z,now -g -Wall -fstack-protector-strong -fPIC" EXTRA_PERFLIBS="-fpie -pie" %{?_smp_mflags} -s V=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_LIBNUMA=1 NO_STRLCPY=1 prefix=%{_prefix}
%if 0%{?with_python2}
%global perf_python2 -C tools/perf PYTHON=%{__python2}
%global perf_python3 -C tools/python3-perf PYTHON=%{__python3}
%else
%global perf_python3 -C tools/perf PYTHON=%{__python3}
%endif

chmod +x tools/perf/check-headers.sh
# perf
%if 0%{?with_python2}
%{perf_make} %{perf_python2} all
%endif

# make sure check-headers.sh is executable
chmod +x tools/python3-perf/check-headers.sh
%{perf_make} %{perf_python3} all

pushd tools/perf/Documentation/
make %{?_smp_mflags} man
popd
%endif

pushd tools/bpf/bpftool
make
popd

chmod +x tools/power/cpupower/utils/version-gen.sh
make %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false
%ifarch %{ix86}
pushd tools/power/cpupower/debug/i386
make %{?_smp_mflags} centrino-decode powernow-k8-decode
popd
%endif
%ifarch x86_64
pushd tools/power/cpupower/debug/x86_64
make %{?_smp_mflags} centrino-decode powernow-k8-decode
popd
%endif
%ifarch %{ix86} x86_64
pushd tools/power/x86/x86_energy_perf_policy/
make
popd
pushd tools/power/x86/turbostat
make
popd
%endif
pushd tools/thermal/tmon/
make
popd
pushd tools/iio/
make
popd
pushd tools/gpio/
make
popd
pushd tools/kvm/kvm_stat/
make %{?_smp_mflags} man
popd

}

install() {
%if 0%{?with_source}
%define _python_bytecompile_errors_terminate_build 0
mkdir -p $RPM_BUILD_ROOT/usr/src/
mv linux-%{KernelVer}-source $RPM_BUILD_ROOT/usr/src/linux-%{KernelVer}
cp linux-%{KernelVer}/.config $RPM_BUILD_ROOT/usr/src/linux-%{KernelVer}/
cp linux-%{KernelVer}/.scmversion $RPM_BUILD_ROOT/usr/src/linux-%{KernelVer}/
%endif

cd linux-%{KernelVer}



mkdir -p $RPM_BUILD_ROOT/boot
dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-%{KernelVer}.img bs=1M count=20

install -m 755 $(make -s image_name) $RPM_BUILD_ROOT/boot/vmlinuz-%{KernelVer}
pushd $RPM_BUILD_ROOT/boot
sha512hmac ./vmlinuz-%{KernelVer} >./.vmlinuz-%{KernelVer}.hmac
popd

install -m 644 .config $RPM_BUILD_ROOT/boot/config-%{KernelVer}
install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-%{KernelVer}

gzip -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-%{KernelVer}.gz

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m 755 %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/mkgrub-menu-%{devel_release}.sh


%if 0%{?with_debuginfo}
mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/%{KernelVer}
cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/%{KernelVer}
%endif

make ARCH=%{Arch} INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=%{KernelVer} mod-fw=
pushd $RPM_BUILD_ROOT/lib/modules/%{KernelVer}
find -type f -name "*.ko" >modnames

xargs --no-run-if-empty chmod u+x < modnames


grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

collect_modules_list()
{
sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
LC_ALL=C sort -u > modules.$1
if [ ! -z "$3" ]; then
sed -r -e "/^($3)\$/d" -i modules.$1
fi
}

collect_modules_list networking \
			 'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt2x00(pci|usb)_probe|register_netdevice'
collect_modules_list block \
		 'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size|ahci_platform_get_resources' 'pktcdvd.ko|dm-mod.ko'
collect_modules_list drm \
			 'drm_open|drm_init'
collect_modules_list modesetting \
			 'drm_crtc_init'

rm -f modinfo
while read i
do
echo -n "$i " >> modinfo
/sbin/modinfo -l $i >> modinfo
done < modnames

grep -E -v \
	  'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' \
  modinfo && exit 1

rm -f modinfo modnames drivers.undef

for i in alias alias.bin builtin.bin ccwmap dep dep.bin ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols symbols.bin usbmap
do
rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$i
done
popd
%define __modsign_install_post \
    if [ "%{with_signmodules}" -eq "1" ];then \
        cp certs/signing_key.pem . \
        cp certs/signing_key.x509 . \
        chmod 0755 %{modsign_cmd} \
        %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KernelVer} || exit 1 \
    fi \
    find $RPM_BUILD_ROOT/lib/modules/ -type f -name '*.ko' | xargs -n1 -P`nproc --all` xz; \
%{nil}

make ARCH=%{Arch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr KBUILD_SRC= headers_install
make ARCH=%{Arch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_check
find $RPM_BUILD_ROOT/usr/include -name "\.*"  -exec rm -rf {} \;

%ifarch aarch64
mkdir -p $RPM_BUILD_ROOT/boot/dtb-%{KernelVer}
install -m 644 $(find arch/%{Arch}/boot -name "*.dtb") $RPM_BUILD_ROOT/boot/dtb-%{KernelVer}/
rm -f $(find arch/$Arch/boot -name "*.dtb")
%endif

make -s ARCH=%{Arch} INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=%{KernelVer}
if [ ! -s ldconfig-kernel.conf ]; then
echo "# Placeholder file, no vDSO hwcap entries used in this kernel." >ldconfig-kernel.conf
fi
install -D -m 444 ldconfig-kernel.conf $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-%{KernelVer}.conf

rm -f $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build
rm -f $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/source
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/extra
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/updates
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/weak-updates
find -type f \( -name "Makefile*" -o -name "Kconfig*" \) -exec cp --parents {} $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build \;
for f in Module.symvers System.map Module.markers .config;do
test -f $f || continue
cp $f $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build
done

cp -a scripts $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build
if [ -d arch/%{Arch}/scripts ]; then
cp -a arch/%{Arch}/scripts $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/arch/%{_arch} || :
fi
if [ -f arch/%{Arch}/*lds ]; then
cp -a arch/%{Arch}/*lds $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/arch/%{_arch}/ || :
fi
find $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/scripts/ -name "*.o" -exec rm -rf {} \;

if [ -d arch/%{Arch}/include ]; then
cp -a --parents arch/%{Arch}/include $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/
fi
cp -a include $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/include

if [ -f arch/%{Arch}/kernel/module.lds ]; then
cp -a --parents arch/%{Arch}/kernel/module.lds $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/
fi

if [ -f scripts/module.lds ]; then
cp -a --parents scripts/module.lds $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/
fi

%ifarch aarch64
cp -a --parents arch/arm/include/asm $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/
%endif

if grep -q CONFIG_STACK_VALIDATION=y .config; then
mkdir -p $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/tools/objtool
cp -a tools/objtool/objtool $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/tools/objtool
fi

touch -r $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/Makefile $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/include/generated/uapi/linux/version.h
touch -r $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/.config $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/include/generated/autoconf.h
if [ ! -f $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/include/config/auto.conf ];then
cp .config $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build/include/config/auto.conf
fi

mkdir -p %{buildroot}/usr/src/kernels
mv $RPM_BUILD_ROOT/lib/modules/%{KernelVer}/build $RPM_BUILD_ROOT/usr/src/kernels/%{KernelVer}

find $RPM_BUILD_ROOT/usr/src/kernels/%{KernelVer} -name ".*.cmd" -exec rm -f {} \;

pushd $RPM_BUILD_ROOT/lib/modules/%{KernelVer}
ln -sf /usr/src/kernels/%{KernelVer} build
ln -sf build source
popd






%if %{with_perf}
# perf
# perf tool binary and supporting scripts/binaries
%if 0%{?with_python2}
%{perf_make} %{perf_python2} DESTDIR=%{buildroot} lib=%{_lib} install-bin install-traceevent-plugins
%else
%{perf_make} %{perf_python3} DESTDIR=%{buildroot} lib=%{_lib} install-bin install-traceevent-plugins
%endif
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace

# remove examples
rm -rf %{buildroot}/usr/lib/perf/examples
# remove the stray header file that somehow got packaged in examples
rm -rf %{buildroot}/usr/lib/perf/include/bpf/

# python-perf extension
%{perf_make} %{perf_python3} DESTDIR=%{buildroot} install-python_ext
%if 0%{?with_python2}
%{perf_make} %{perf_python2} DESTDIR=%{buildroot} install-python_ext
%endif

# perf man pages (note: implicit rpm magic compresses them later)
install -d %{buildroot}/%{_mandir}/man1
install -pm0644 tools/kvm/kvm_stat/kvm_stat.1 %{buildroot}/%{_mandir}/man1/
install -pm0644 tools/perf/Documentation/*.1 %{buildroot}/%{_mandir}/man1/
%endif

pushd tools/bpf/bpftool
make DESTDIR=%{buildroot} prefix=%{_prefix} bash_compdir=%{_sysconfdir}/bash_completion.d/ mandir=%{_mandir} install doc-install
popd
make -C tools/power/cpupower DESTDIR=%{buildroot} libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
rm -f %{buildroot}%{_libdir}/*.{a,la}
%find_lang cpupower
mv cpupower.lang ../
%ifarch %{ix86}
pushd tools/power/cpupower/debug/i386
install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
popd
%endif
%ifarch x86_64
pushd tools/power/cpupower/debug/x86_64
install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE8} %{buildroot}%{_unitdir}/cpupower.service
install -m644 %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/cpupower
%ifarch %{ix86} x86_64
mkdir -p %{buildroot}%{_mandir}/man8
pushd tools/power/x86/x86_energy_perf_policy
make DESTDIR=%{buildroot} install
popd
pushd tools/power/x86/turbostat
make DESTDIR=%{buildroot} install
popd
%endif
pushd tools/thermal/tmon
make INSTALL_ROOT=%{buildroot} install
popd
pushd tools/iio
make DESTDIR=%{buildroot} install
popd
pushd tools/gpio
make DESTDIR=%{buildroot} install
popd
pushd tools/kvm/kvm_stat
make INSTALL_ROOT=%{buildroot} install-tools
popd

%define __spec_install_post\
%{?__debug_package:%{__debug_install_post}}\
%{__arch_install_post}\
%{__os_install_post}\
%{__modsign_install_post}\
%{nil}

}

