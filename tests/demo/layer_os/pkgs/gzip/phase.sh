#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%ifarch aarch64
export CFLAGS="${CFLAGS:-%optflags} -march=armv8-a+crc"
%endif
autoreconf
%configure
%make_build

}

install() {
rm -rf %RPM_BUILD_ROOT
%make_install
rm -f %{buildroot}%{_bindir}/uncompress

%global profiledir %{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE1} %{buildroot}%{profiledir}
install -p -m 644 %{SOURCE2} %{buildroot}%{profiledir}

}

check() {
make check

}

