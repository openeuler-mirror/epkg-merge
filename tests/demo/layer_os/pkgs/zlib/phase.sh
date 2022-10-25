#!/usr/bash

prep() {
%setup -n %{name}-%{version}
%patch0 -p1
%ifarch aarch64
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%endif
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

}

build() {
export CFLAGS="$RPM_OPT_FLAGS"
%ifarch aarch64
CFLAGS+=" -DARM_NEON -O3"
CFLAGS+=" -march=armv8-a+crc"
%endif

./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
%make_build LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now"

cd contrib/minizip
autoreconf --install
%configure %%{env.configureFlags}
%make_build

}

install() {
%make_install

%make_install -C contrib/minizip
rm -f $RPM_BUILD_ROOT%_includedir/minizip/crypt.h

find $RPM_BUILD_ROOT -name '*.la' | xargs rm -f

}

check() {
make test

}

