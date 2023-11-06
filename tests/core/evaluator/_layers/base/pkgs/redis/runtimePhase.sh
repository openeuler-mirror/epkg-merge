#!/usr/bin/env bash

pre() {
    getent group %{name} &> /dev/null || \
    groupadd -r %{name} &> /dev/null
    getent passwd %{name} &> /dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c 'Redis Database Server' %{name} &> /dev/null
    exit 0
}

post() {
    %systemd_post %{name}.service
    %systemd_post %{name}-sentinel.service
}

preun() {
    %systemd_preun %{name}.service
    %systemd_preun %{name}-sentinel.service
}

postun() {
    %systemd_postun_with_restart %{name}.service
    %systemd_postun_with_restart %{name}-sentinel.service
}

