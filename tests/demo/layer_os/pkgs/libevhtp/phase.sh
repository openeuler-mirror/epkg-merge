#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
mkdir -p build
cd build
%cmake -DEVHTP_BUILD_SHARED=ON -DEVHTP_DISABLE_SSL=ON -DLIB_INSTALL_DIR=lib ..
%make_build

}

install() {
rm -rf %{buildroot}
cd build
%make_install

%delete_la_and_a
find %{buildroot} -name '*.cmake' -exec rm -f {} ';'
find %{buildroot} -name '*.so.*' -exec strip {} ';'

%ldconfig_scriptlets

}

