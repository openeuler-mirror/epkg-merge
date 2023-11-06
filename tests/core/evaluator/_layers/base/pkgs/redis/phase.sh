#!/usr/bin/env bash

prep() {
    %setup
    %patch0001 -p1
    %patch0002 -p1
    %patch0003 -p1
    %patch0004 -p1
    %ifarch aarch64
    %patch0005 -p1
    %endif
    %patch0006 -p1
    %patch0007 -p1
    %patch0008 -p1
    %patch0009 -p1
    %patch0010 -p1
    %ifarch sw_64
    %patch0011 -p1
    %endif
    %patch0012 -p1
    %patch0013 -p1
    %patch0014 -p1
    %ifarch loongarch64
    %_update_config_guess
    %_update_config_sub
    %endif
    
    sed -i -e 's|^logfile .*$|logfile /var/log/redis2/redis2.log|g' redis2.conf
    sed -i -e '$ alogfile /var/log/redis2/sentinel.log' sentinel.conf
    sed -i -e 's|^dir .*$|dir /var/lib/redis2|g' redis2.conf
}

build() {
    make
}

install() {
    %make_install PREFIX=%{buildroot}%{_prefix}
    install -d %{buildroot}%{_sharedstatedir}/%{name}
    install -d %{buildroot}%{_localstatedir}/log/%{name}
    install -d %{buildroot}%{_localstatedir}/run/%{name}
    install -d %{buildroot}%{_libdir}/%{name}/modules
    install -pDm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
    mkdir -p %{buildroot}%{_unitdir}
    install -pm644 %{SOURCE2} %{buildroot}%{_unitdir}
    install -pm644 %{SOURCE3} %{buildroot}%{_unitdir}
    install -pDm640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
    install -pDm640 sentinel.conf %{buildroot}%{_sysconfdir}/%{name}-sentinel.conf
}

