#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
mkdir build
cd build
%cmake ..
%make_build VERBOSE=1

}

install() {
rm -rf $RPM_BUILD_ROOT
cd build
%make_install

}

check() {
cd test/parsing
./run_tests.sh
cd ../api
./run_tests.sh

}

