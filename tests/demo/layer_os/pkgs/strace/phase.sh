#!/usr/bash

prep() {
%autosetup -p1
echo -n %version-%release > .tarball-version
echo -n 2020 > .year
echo -n 2020-04-06 > .strace.1.in.date

}

build() {
echo 'BEGIN OF BUILD ENVIRONMENT INFORMATION'
uname -a |head -1
libc="$(ldd /bin/sh |sed -n 's|^[^/]*\(/[^ ]*/libc\.so[^ ]*\).*|\1|p' |head -1)"
$libc |head -1
file -L /bin/sh
gcc --version |head -1
ld --version |head -1
kver="$(printf '%%s\n%%s\n' '#include <linux/version.h>' 'LINUX_VERSION_CODE' | gcc -E -P -)"
printf 'kernel-headers %%s.%%s.%%s\n' $(($kver/65536)) $(($kver/256%%256)) $(($kver%%256))
echo 'END OF BUILD ENVIRONMENT INFORMATION'

CFLAGS_FOR_BUILD="$RPM_OPT_FLAGS"; export CFLAGS_FOR_BUILD
%configure %%{env.configureFlags}
make %{?_smp_mflags}

}

install() {
make DESTDIR=%{buildroot} install

rm -f %{buildroot}%{_bindir}/strace-graph

for f in ChangeLog ChangeLog-CVS; do
gzip -9n < "$f" > "$f".gz &
done
wait

}

check() {

}

