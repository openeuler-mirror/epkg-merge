#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
autoreconf -fi
%configure %%{env.configureFlags}
make


}

install() {
%make_install

install -D -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/quota_nld.service
install -D -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/quota_nld
install -D -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/rpc-rquotad.service
install -D -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rpc-rquotad

%find_lang %{name}

}

check() {
make check


}

