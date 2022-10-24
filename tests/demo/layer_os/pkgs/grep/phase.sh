#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure %%{env.configureFlags} \
CPPFLAGS="-I%{_includedir}/pcre2" CFLAGS="$RPM_OPT_FLAGS -fsigned-char"
%make_build

}

install() {
%make_install
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

install -pm 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -Dpm 755 %{SOURCE3} $RPM_BUILD_ROOT%{_libexecdir}/grepconf.sh

}

check() {
make check

}

