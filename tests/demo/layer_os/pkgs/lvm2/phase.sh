#!/usr/bash

prep() {
%autosetup -n LVM2.%{version} -p1

}

build() {
%configure %%{env.configureFlags} %{?configure_cluster} %{?configure_cmirror} %{?configure_lockd_dlm} %{?configure_lockd_sanlock} 
make %{?_smp_mflags}

}

check() {
make run-unit-test

}

install() {
make install DESTDIR=%{buildroot}
make install_system_dirs DESTDIR=%{buildroot}
make install_systemd_units DESTDIR=%{buildroot}
make install_systemd_generators DESTDIR=%{buildroot}
make install_tmpfiles_configuration DESTDIR=%{buildroot}
make -C test install DESTDIR=%{buildroot}

}

