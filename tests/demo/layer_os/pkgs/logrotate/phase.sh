#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
mkdir build && cd build
%configure %%{env.configureFlags}
%make_build V=1

}

install() {
%make_install -C build

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
mkdir -p %{buildroot}%{_localstatedir}/lib/logrotate

install -p -m 644 examples/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.conf
install -p -m 644 examples/*tmp %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 755 examples/logrotate.cron %{buildroot}%{_sysconfdir}/cron.daily/logrotate

}

check() {
%make_build -C build check

}

