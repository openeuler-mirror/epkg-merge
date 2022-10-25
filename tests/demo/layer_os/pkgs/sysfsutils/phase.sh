#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
./autogen
%configure %%{env.configureFlags} --libdir=/%{_lib}
%make_build

}

check() {
make check

}

install() {
%make_install

rm -f %{buildroot}/%{_bindir}/dlist_test
rm -f %{buildroot}/%{_bindir}/get_device
rm -f %{buildroot}/%{_bindir}/get_driver
rm -f %{buildroot}/%{_lib}/libsysfs.la

chrpath -d  $(find $RPM_BUILD_ROOT -name get_module)
chrpath -d  $(find $RPM_BUILD_ROOT -name systool)

%ldconfig_scriptlets

}

