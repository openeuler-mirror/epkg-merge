#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%define _build_arg0__ CFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 $RPM_OPT_FLAGS" SUID_CFLAGS="-fpie"
%define _build_arg1__ SUID_LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now" DAEMON_CFLAGS="$SUID_CFLAGS" DAEMON_LDFLAGS="$SUID_LDFLAGS"

unset LINGUAS || :
%configure %%{env.configureFlags}

%make_build %{_build_arg0__} %{_build_arg1__}

}

check() {
make check

}

install() {
%make_install

install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}{/run/uuidd,/var/lib/libuuid,/var/log}

mv %{buildroot}%{_sbindir}/raw %{buildroot}%{_bindir}/raw
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/login
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/remote
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/chsh
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/chfn
install -Dm644 %{SOURCE4} %{buildroot}%{_prefix}/lib/udev/rules.d/60-raw.rules
install -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/adjtime
install -m644 %{SOURCE6} %{buildroot}%{_sysconfdir}/pam.d/su
install -m644 %{SOURCE7} %{buildroot}%{_sysconfdir}/pam.d/su-l
install -m644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/runuser
install -m644 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/runuser-l

ln -sf hwclock %{buildroot}%{_sbindir}/clock
ln -sf ../proc/self/mounts %{buildroot}/etc/mtab

touch %{buildroot}/var/log/lastlog
chmod 0644 %{buildroot}/var/log/lastlog

echo ".so man8/raw.8" > %{buildroot}%{_mandir}/man8/rawdevices.8
echo ".so man8/hwclock.8" > %{buildroot}%{_mandir}/man8/clock.8

%find_lang %name

find  %{buildroot}%{_bindir}/ -regextype posix-egrep -type l \
  -regex ".*(linux32|linux64|aarch64|i386|x86_64|uname26)$" \
  -printf "%{_bindir}/%f\n" > %{name}.files
cat %{name}.lang >> %{name}.files

find  %{buildroot}%{_mandir}/man8 -regextype posix-egrep  \
  -regex ".*(linux32|linux64|aarch64|i386|x86_64|uname26)\.8.*" \
  -printf "%{_mandir}/man8/%f*\n" > %{name}-help.files

rm -rf %{buildroot}%{_libdir}/*.{la,a}
rm -rf %{buildroot}%{_libdir}/python*/site-packages/*.{la,a}

}

