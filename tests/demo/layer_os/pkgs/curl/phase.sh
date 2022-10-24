#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

printf "1112\n1455\n1184\n1801\n1592\n" >> tests/data/DISABLED

sed -e 's/^35$/35,52/' -i tests/data/test323
(
{ set +x; } 2>/dev/null
cmd="sed -e 's|ip6-localhost|localhost6|' -i tests/data/test[0-9]*"
printf "+ %s\n" "$cmd" >&2
eval "$cmd"
)

aclocal -I m4
automake

}

build() {
install -d build-full
export common_configure_opts="--cache-file=../config.cache \
    --enable-symbol-hiding  --enable-ipv6  --enable-threaded-resolver \
    --with-gssapi  --with-nghttp2  --with-ssl \
    --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt"

%global _configure ../configure

(
cd build-full
%configure $common_configure_opts %%{env.configureFlags}
)

sed -e 's/^runpath_var=.*/runpath_var=/' \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/' \
    -i build-full/libtool

%make_build V=1 -C build-full

}

check() {
%make_build V=1 -C build-full/tests

export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=XXX
export OPENSSL_CONF=

export srcdir=../../tests

unset DEBUGINFOD_URLS

for size in full; do (
cd build-${size}

export LD_LIBRARY_PATH="${PWD}/lib/.libs"

cd tests
perl -I../../tests ../../tests/runtests.pl -a -p -v '!flaky'
)
done

}

install() {
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.{la,so}

install -D -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal/libcurl.m4

cd build-full
%make_install

LD_LIBRARY_PATH="$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH" %make_install -C scripts

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/fish

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.a
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la

%ldconfig_scriptlets

%ldconfig_scriptlets -n libcurl

}

