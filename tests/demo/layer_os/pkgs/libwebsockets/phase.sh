#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1
}

build() {
mkdir -p build
cd build
%cmake \
    -D LWS_WITH_HTTP2=ON \
    -D LWS_IPV6=ON \
    -D LWS_WITH_ZIP_FOPS=ON \
    -D LWS_WITH_SOCKS5=ON \
    -D LWS_WITH_RANGES=ON \
    -D LWS_WITH_ACME=ON \
    -D LWS_WITH_LIBUV=OFF \
    -D LWS_WITH_LIBEV=OFF \
    -D LWS_WITH_LIBEVENT=OFF \
    -D LWS_WITH_FTS=ON \
    -D LWS_WITH_THREADPOOL=ON \
    -D LWS_UNIX_SOCK=ON \
    -D LWS_WITH_HTTP_PROXY=ON \
    -D LWS_WITH_DISKCACHE=ON \
    -D LWS_WITH_LWSAC=ON \
    -D LWS_LINK_TESTAPPS_DYNAMIC=ON \
    -D LWS_WITHOUT_BUILTIN_GETIFADDRS=ON \
    -D LWS_USE_BUNDLED_ZLIB=OFF \
    -D LWS_WITHOUT_BUILTIN_SHA1=ON \
    -D LWS_WITH_STATIC=OFF \
    -D LWS_WITHOUT_CLIENT=OFF \
    -D LWS_WITHOUT_SERVER=OFF \
    -D LWS_WITHOUT_TESTAPPS=OFF \
    -D LWS_WITHOUT_TEST_SERVER=ON \
    -D LWS_WITHOUT_TEST_SERVER_EXTPOLL=ON \
    -D LWS_WITHOUT_TEST_PING=ON \
    -D LWS_WITHOUT_TEST_CLIENT=ON \
    -D LWS_WITHOUT_EXTENSIONS=OFF \
    ..

%make_build

}

install() {
cd build
%make_install

%delete_la_and_a
find %{buildroot} -name '*.cmake' -exec rm -f {} ';'
find %{buildroot} -name '*_static.pc' -exec rm -f {} ';'

%ldconfig_scriptlets

}

