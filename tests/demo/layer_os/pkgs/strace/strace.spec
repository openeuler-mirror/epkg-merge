#needsrootforbuild
# This spec file is from upstream.
Summary: Tracks and displays system calls associated with a running process
Name: strace
Version: 5.14
Release: 1
# The test suite is GPLv2+, all the rest is LGPLv2.1+.
License: LGPL-2.1+ and GPL-2.0+
# Some distros require Group tag to be present,
# some require Group tag to be absent,
# some do not care about Group tag at all,
# and we have to cater for all of them.
URL: https://strace.io
%if 0%{?fedora} >= 12 || 0%{?centos} >= 6 || 0%{?rhel} >= 6 || 0%{?suse_version} >= 1200 || 0%{?openEuler} >= 1
Source: https://strace.io/files/%{version}/strace-%{version}.tar.xz
BuildRequires: xz
%else
Source: strace-%{version}.tar.gz
%endif
BuildRequires: gcc gzip

# Install Bluetooth headers for AF_BLUETOOTH sockets decoding.
%if 0%{?fedora} >= 18 || 0%{?centos} >= 6 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1200 || 0%{?openEuler} >= 1
BuildRequires: pkgconfig(bluez)
%endif

# Install elfutils-devel or libdw-devel to enable strace -k option.
# Install binutils-devel to enable symbol demangling.
%if 0%{?fedora} >= 20 || 0%{?centos} >= 6 || 0%{?rhel} >= 6 || 0%{?openEuler} >= 1
%define buildrequires_stacktrace BuildRequires: elfutils-devel binutils-devel
%endif
%if 0%{?suse_version} >= 1100
%define buildrequires_stacktrace BuildRequires: libdw-devel binutils-devel
%endif
%{?buildrequires_stacktrace}

# OBS compatibility
%{?!buildroot:BuildRoot: %_tmppath/buildroot-%name-%version-%release}
%define maybe_use_defattr %{?suse_version:%%defattr(-,root,root)}

%description
The strace program intercepts and records the system calls called and
received by a running process.  Strace can print a record of each
system call, its arguments and its return value.  Strace is useful for
diagnosing problems and debugging, as well as for instructional
purposes.

Install strace if you need a tool to track the system calls made and
received by a process.

%prep
%autosetup -p1
echo -n %version-%release > .tarball-version
echo -n 2020 > .year
echo -n 2020-04-06 > .strace.1.in.date

%build
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
%configure --enable-mpers=check
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_bindir}/strace-graph

# some say uncompressed changelog files are too big
for f in ChangeLog ChangeLog-CVS; do
	gzip -9n < "$f" > "$f".gz &
done
wait

%check
# testcases which read /dev/full will fail because /dev/full is rw--w--w-- and
# needsrootforbuild cannot take affect
#%{buildroot}%{_bindir}/strace -V
#make %{?_smp_mflags} -k check VERBOSE=1
#echo 'BEGIN OF TEST SUITE INFORMATION'
#tail -n 99999 -- tests*/test-suite.log tests*/ksysent.gen.log
#find tests* -type f -name '*.log' -print0 |
#	xargs -r0 grep -H '^KERNEL BUG:' -- ||:
#echo 'END OF TEST SUITE INFORMATION'

%files
%maybe_use_defattr
%doc CREDITS ChangeLog.gz ChangeLog-CVS.gz COPYING NEWS README
%{_bindir}/strace
%{_bindir}/strace-log-merge
%{_mandir}/man1/*

%changelog
* Mon Nov 29 2021 zhouwenpei <zhouwenpei1@huawei.com> - 5.14-1
- update to 5.14

* Mon Feb 1 2021 xinghe <xinghe1@huawei.com> - 5.10-1
- update to 5.10

* Tue Nov 10 2020 xinghe <xinghe1@huawei.com> - 5.6-2
- fix master build error

* Sat Jul 25 2020 liuchao<liuchao173@huawei.com> - 5.6-1
- Upgrade strace version to 5.6

* Wed Jan  8 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0-2
- Upgrade strace version to 5.0

* Tue Mar 19 2019 strace-devel@lists.strace.io - 5.0-1
- strace 5.0 snapshot.
