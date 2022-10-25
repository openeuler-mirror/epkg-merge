#!/usr/bash

prep() {
%setup -q

mkdir -p -m755 kcp
tar -z -x -v -f %{SOURCE8}
tar -z -x -v -f %{SOURCE14}

%ifarch aarch64
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
%ifarch aarch64
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

}

build() {
autoreconf
%configure --sbindir=/usr/sbin \
    CFLAGS="${CFLAGS} -fstack-protector-strong -Wl,-z,now -pie -fPIC -fPIE"
rm -f kexec-tools.spec.in
cp %{SOURCE16} %{SOURCE21} %{SOURCE22} .

make
%ifarch %{ix86} x86_64 aarch64
make -C eppic-%{eppic_ver}/libeppic
make -C makedumpfile-%{mkdf_ver} LINKTYPE=dynamic USELZO=on USESNAPPY=on
make -C makedumpfile-%{mkdf_ver} LDFLAGS="$LDFLAGS -I../eppic-%{eppic_ver}/libeppic -L../eppic-%{eppic_ver}/libeppic" eppic_makedumpfile.so
%endif

}

install() {
mkdir -p -m755 %{buildroot}/usr/sbin
mkdir -p -m755 %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p -m755 %{buildroot}%{_localstatedir}/crash
mkdir -p -m755 %{buildroot}%{_mandir}/man8/
mkdir -p -m755 %{buildroot}%{_mandir}/man5/
mkdir -p -m755 %{buildroot}%{_docdir}
mkdir -p -m755 %{buildroot}%{_datadir}/kdump
mkdir -p -m755 %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p -m755 %{buildroot}%{_bindir}
mkdir -p -m755 %{buildroot}%{_libdir}
mkdir -p -m755 %{buildroot}%{_prefix}/lib/kdump
install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/kdumpctl

install -m 755 build/sbin/kexec %{buildroot}/usr/sbin/kexec
install -m 755 build/sbin/vmcore-dmesg %{buildroot}/usr/sbin/vmcore-dmesg
install -m 644 build/man/man8/kexec.8 %{buildroot}%{_mandir}/man8/
install -m 644 build/man/man8/vmcore-dmesg.8 %{buildroot}%{_mandir}/man8/

SYSCONFIG=%{_sourcedir}/kdump.sysconfig.%{_target_cpu}
[ -f $SYSCONFIG ] || SYSCONFIG=%{_sourcedir}/kdump.sysconfig.%{_arch}
[ -f $SYSCONFIG ] || SYSCONFIG=%{_sourcedir}/kdump.sysconfig
install -m 644 $SYSCONFIG %{buildroot}%{_sysconfdir}/sysconfig/kdump

install -m 755 %{SOURCE6} %{buildroot}/usr/sbin/mkdumprd
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/kdump.conf
install -m 644 kexec/kexec.8 %{buildroot}%{_mandir}/man8/kexec.8
install -m 644 %{SOURCE9} %{buildroot}%{_mandir}/man8/mkdumprd.8
install -m 644 %{SOURCE20} %{buildroot}%{_mandir}/man8/kdumpctl.8
install -m 755 %{SOURCE15} %{buildroot}%{_prefix}/lib/kdump/kdump-lib.sh
install -m 755 %{SOURCE18} %{buildroot}%{_prefix}/lib/kdump/kdump-lib-initramfs.sh
install -m 755 %{SOURCE23} $RPM_BUILD_ROOT%{_udevrulesdir}/../kdump-udev-throttler
install -m 644 %{SOURCE11} %{buildroot}%{_mandir}/man5/kdump.conf.5
install -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/kdump.service
install -m 755 -D %{SOURCE17} %{buildroot}%{_prefix}/lib/systemd/system-generators/kdump-dep-generator.sh
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_udevrulesdir}/98-kexec.rules

%ifarch %{ix86} x86_64 aarch64
install -m 755 makedumpfile-%{mkdf_ver}/makedumpfile $RPM_BUILD_ROOT/usr/sbin/makedumpfile
install -m 644 makedumpfile-%{mkdf_ver}/makedumpfile.8.gz $RPM_BUILD_ROOT/%{_mandir}/man8/makedumpfile.8.gz
install -m 644 makedumpfile-%{mkdf_ver}/makedumpfile.conf.5.gz $RPM_BUILD_ROOT/%{_mandir}/man5/makedumpfile.conf.5.gz
install -m 644 makedumpfile-%{mkdf_ver}/makedumpfile.conf $RPM_BUILD_ROOT/%{_sysconfdir}/makedumpfile.conf.sample
install -m 755 makedumpfile-%{mkdf_ver}/eppic_makedumpfile.so $RPM_BUILD_ROOT/%{_libdir}/eppic_makedumpfile.so
mkdir -p $RPM_BUILD_ROOT/usr/share/makedumpfile/eppic_scripts/
install -m 644 makedumpfile-%{mkdf_ver}/eppic_scripts/* $RPM_BUILD_ROOT/usr/share/makedumpfile/eppic_scripts/
%endif

%define remove_dracut_prefix() %(echo -n %1|sed 's/.*dracut-//g')
%define remove_dracut_early_kdump_prefix() %(echo -n %1|sed 's/.*dracut-early-kdump-//g')

mkdir -p -m755 %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase
cp %{SOURCE25} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE25}}
cp %{SOURCE26} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE26}}
cp %{SOURCE27} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE27}}
cp %{SOURCE28} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE28}}
cp %{SOURCE29} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE29}}
cp %{SOURCE30} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE30}}
cp %{SOURCE31} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE31}}
cp %{SOURCE32} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE32}}
cp %{SOURCE35} $RPM_BUILD_ROOT/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE35}}
chmod 755 %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE25}}
chmod 755 %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE26}}
mkdir -p -m755 %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99earlykdump
cp %{SOURCE33} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99earlykdump/%{remove_dracut_prefix %{SOURCE33}}
cp %{SOURCE34} %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99earlykdump/%{remove_dracut_early_kdump_prefix %{SOURCE34}}
chmod 755 %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99earlykdump/%{remove_dracut_prefix %{SOURCE33}}
chmod 755 %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99earlykdump/%{remove_dracut_early_kdump_prefix %{SOURCE34}}
chmod 755 %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/99kdumpbase/%{remove_dracut_prefix %{SOURCE28}}

%define dracutlibdir %{_prefix}/lib/dracut
mkdir -p %{buildroot}/%{dracutlibdir}/modules.d/
mv %{buildroot}/etc/kdump-adv-conf/kdump_dracut_modules/* %{buildroot}/%{dracutlibdir}/modules.d/

}

