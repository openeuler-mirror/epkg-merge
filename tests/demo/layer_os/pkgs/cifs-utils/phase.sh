#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
autoreconf -vif
%configure  --prefix=/usr %%{env.configureFlags} ROOTSBINDIR=%{_sbindir}
make %{?_smp_mflags}

}

install() {
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
ln -s %{_libdir}/%{name}/idmapwb.so %{buildroot}%{_sysconfdir}/%{name}/idmap-plugin
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d

}

