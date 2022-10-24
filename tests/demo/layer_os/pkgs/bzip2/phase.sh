#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%make_build -f Makefile-libbz2_so "CFLAGS=%{optflags} -Winline -fpic -fPIC -D_FILE_OFFSET_BITS=64"
%make_build "CFLAGS=%{optflags} -fpic -fPIC -Winline -D_FILE_OFFSET_BITS=64"

}

install() {
rm -rf %RPM_BUILD_ROOT
%make_install PREFIX=%{buildroot}%{_prefix}

pushd %{buildroot}%{_prefix}
mkdir -p share
mv man/ share/
mv lib lib64
popd

ln -fs bzdiff %{buildroot}%{_bindir}/bzcmp
ln -fs bzgrep %{buildroot}%{_bindir}/bzegrep
ln -fs bzgrep %{buildroot}%{_bindir}/bzfgrep
ln -fs bzmore %{buildroot}%{_bindir}/bzless
install -m 0755 libbz2.so.%{version}  %{buildroot}%{_libdir}
ln -s libbz2.so.%{version} %{buildroot}%{_libdir}/libbz2.so.1
ln -s libbz2.so.1 %{buildroot}%{_libdir}/libbz2.so
cp %{SOURCE1} .
sed -i "s@^libdir=@libdir=%{_libdir}@" bzip2.pc
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m 0644 bzip2.pc %{buildroot}%{_libdir}/pkgconfig/
ln -s bzip2.1.gz %{buildroot}%{_mandir}/man1/bunzip2.1.gz
ln -s bzip2.1.gz %{buildroot}%{_mandir}/man1/bzcat.1.gz
ln -s bzip2.1.gz %{buildroot}%{_mandir}/man1/bzip2recover.1.gz

}

check() {
make check

%ldconfig_scriptlets

}

