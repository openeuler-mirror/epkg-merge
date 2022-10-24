#!/usr/bash

prep() {
%autosetup -p 1  -n selinux-policycoreutils-%{version}

}

build() {
%set_build_flags
export PYTHON=%{__python3}

make -C policycoreutils LSPP_PRIV=y SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="%{_sbindir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C python  SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C semodule-utils  SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C restorecond     SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
%if %{with sandbox}
make -C sandbox SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
%endif
make -C dbus    SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all

}

install() {
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}/
make -C policycoreutils LSPP_PRIV=y  DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" install
make -C python  PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make -C semodule-utils  PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make -C restorecond     PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
%if %{with sandbox}
make -C sandbox PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
%endif
make -C dbus    PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install


rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/restorecond
rm -f %{buildroot}/%{_sbindir}/open_init_pty
rm -f %{buildroot}/%{_sbindir}/run_init
rm -f %{buildroot}/%{_mandir}/man8/open_init_pty.8
rm -f %{buildroot}/%{_mandir}/ru/man8/run_init.8*
rm -f %{buildroot}/%{_mandir}/man8/run_init.8*
rm -f %{buildroot}/etc/pam.d/run_init*

rm -f  %{buildroot}%{python3_sitelib}/sepolicy/gui.*
rm -f  %{buildroot}%{python3_sitelib}/sepolicy/sepolicy.glade

install -m 644 -p %{SOURCE2} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE3} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE4} %{buildroot}/%{_unitdir}/
install -D -m 755 -p %{SOURCE5} %{buildroot}/%{_systemdgeneratordir}/%{basename:%{SOURCE5}}
install -m 755 -p %{SOURCE1} %{buildroot}/%{_libexecdir}/selinux/

pathfix.py -i "%{__python3} -Es" -p %{buildroot}%{python3_sitelib}
pathfix.py -i "%{__python3} -Es" -p %{buildroot}%{_sbindir}/semanage \
%if %{with sandbox}
%{buildroot}%{_bindir}/sandbox \
    %{buildroot}%{_datadir}/sandbox/start \
    %endif
%{buildroot}%{_bindir}/chcat  %{buildroot}%{_bindir}/audit2allow \
    %{buildroot}%{_bindir}/sepolicy   %{buildroot}%{_bindir}/sepolgen-ifgen \
    %{buildroot}%{_datadir}/system-config-selinux/selinux_server.py


find %{buildroot}%{python3_sitelib} %{buildroot}%{python3_sitearch} \
    %{buildroot}%{_sbindir} %{buildroot}%{_bindir} %{buildroot}%{_datadir} -type f -name '*~' | xargs rm -f

%py_byte_compile %{__python3} %{buildroot}%{_datadir}/system-config-selinux

%find_lang policycoreutils

%endif
}

