#!/usr/bash

prep() {
%autosetup -p1

}

build() {
autoreconf -ifv
if as --help | grep -q execstack; then
export CCAS="gcc -c -Wa,--noexecstack"
fi

%ifarch %{ix86}
export CFLAGS=$(echo %{optflags} | sed -e "s/-mtune=[^ ]*//g" | sed -e "s/-march=[^ ]*/-march=i686/g")
export CXXFLAGS=$(echo %{optflags} | sed -e "s/-mtune=[^ ]*//g" | sed -e "s/-march=[^ ]*/-march=i686/g")
%endif

%configure %%{env.configureFlags}

sed -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|-lstdc++ -lm|-lstdc++|' \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -i libtool
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags}

}

install() {
export LD_LIBRARY_PATH=`pwd`/.libs
make install DESTDIR=$RPM_BUILD_ROOT
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{gmp,mp,gmpxx}.la
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf libgmpxx.so.4 $RPM_BUILD_ROOT%{_libdir}/libgmpxx.so

basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif

}

check() {
export LD_LIBRARY_PATH=`pwd`/.libs
make %{?_smp_mflags} check

}

