#!/usr/bash

prep() {
%autosetup -n iSulad-v%{_version} -Sgit -p1

}

build() {
mkdir -p build
cd build
%if 0%{?enable_shimv2}
%cmake -DDEBUG=ON -DCMAKE_SKIP_RPATH=TRUE -DLIB_INSTALL_DIR=%{_libdir} -DCMAKE_INSTALL_PREFIX=/usr -DENABLE_SHIM_V2=ON ../
%else
%cmake -DDEBUG=ON -DCMAKE_SKIP_RPATH=TRUE -DLIB_INSTALL_DIR=%{_libdir} -DCMAKE_INSTALL_PREFIX=/usr ../
%endif
%make_build

}

install() {
rm -rf %{buildroot}
cd build
install -d $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 ./src/libisula.so             %{buildroot}/%{_libdir}/libisula.so
install -m 0755 ./src/utils/http/libhttpclient.so  %{buildroot}/%{_libdir}/libhttpclient.so
install -m 0755 ./src/libisulad_tools.so  %{buildroot}/%{_libdir}/libisulad_tools.so
install -m 0755 ./src/daemon/modules/image/libisulad_img.so   %{buildroot}/%{_libdir}/libisulad_img.so

install -d $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
install -m 0640 ./conf/isulad.pc              %{buildroot}/%{_libdir}/pkgconfig/isulad.pc

install -d $RPM_BUILD_ROOT/%{_bindir}

install -m 0755 ./src/isula                  %{buildroot}/%{_bindir}/isula
install -m 0755 ./src/isulad-shim            %{buildroot}/%{_bindir}/isulad-shim

install -m 0755 ./src/isulad                 %{buildroot}/%{_bindir}/isulad

install -d $RPM_BUILD_ROOT/%{_includedir}/isulad
install -m 0644 ../src/daemon/modules/api/image_api.h         %{buildroot}/%{_includedir}/isulad/image_api.h

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/isulad
install -m 0640 ../src/contrib/config/daemon.json           %{buildroot}/%{_sysconfdir}/isulad/daemon.json
install -m 0440 ../src/contrib/config/daemon_constants.json %{buildroot}/%{_sysconfdir}/isulad/daemon_constants.json
install -m 0640 ../src/contrib/config/seccomp_default.json  %{buildroot}/%{_sysconfdir}/isulad/seccomp_default.json

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/default/isulad
install -m 0640 ../src/contrib/config/config.json           %{buildroot}/%{_sysconfdir}/default/isulad/config.json
install -m 0640 ../src/contrib/config/systemcontainer_config.json           %{buildroot}/%{_sysconfdir}/default/isulad/systemcontainer_config.json
install -m 0550 ../src/contrib/sysmonitor/isulad-check.sh        %{buildroot}/%{_sysconfdir}/default/isulad/isulad-check.sh

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysmonitor/process
cp ../src/contrib/sysmonitor/isulad-monit $RPM_BUILD_ROOT/etc/sysmonitor/process

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/default/isulad/hooks
install -m 0640 ../src/contrib/config/hooks/default.json %{buildroot}/%{_sysconfdir}/default/isulad/hooks/default.json

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
install -p -m 0640 ../src/contrib/config/iSulad.sysconfig $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/iSulad

%if 0%{?is_systemd}
install -d $RPM_BUILD_ROOT/%{_unitdir}
install -p -m 0640 ../src/contrib/init/isulad.service $RPM_BUILD_ROOT/%{_unitdir}/isulad.service
%else
install -d $RPM_BUILD_ROOT/%{_initddir}
install -p -m 0640 ../src/contrib/init/isulad.init $RPM_BUILD_ROOT/%{_initddir}/isulad.init
%endif

}

clean() {
rm -rf %{buildroot}

}

