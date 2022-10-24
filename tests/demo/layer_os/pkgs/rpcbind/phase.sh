#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
autoreconf -fisv
%configure --sbindir=%{_bindir} %%{env.configureFlags}

make all

}

install() {
install -m 0755 -d %{buildroot}{%{_sbindir},%{_bindir},/etc/sysconfig}
install -m 0755 -d %{buildroot}%{_unitdir}
install -m 0755 -d %{buildroot}%{_tmpfilesdir}
install -m 0755 -d %{buildroot}%{_mandir}/man8
install -m 0755 -d %{buildroot}%{rpcbind_state_dir}
%make_install
make DESTDIR=$RPM_BUILD_ROOT install

install -m 644 %{SOURCE1} %{buildroot}/etc/sysconfig/%{name}

cd %{buildroot}%{_sbindir}
ln -sf ../bin/%{name}
ln -sf ../bin/rpcinfo

}

