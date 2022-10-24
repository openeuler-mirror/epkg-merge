#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
rm -f ./configure
autoreconf -ivf
%configure
%make_build CFLAGS="%{optflags} -D_GNU_SOURCE -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"

}

install() {
%make_install


}

