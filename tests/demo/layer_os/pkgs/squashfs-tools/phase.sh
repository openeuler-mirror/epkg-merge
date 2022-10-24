#!/usr/bash

prep() {
%autosetup -n squashfs-tools-%{version} -p1

}

build() {
CFLAGS="%{optflags}" XZ_SUPPORT=1 LZO_SUPPORT=1 LZMA_XZ_SUPPORT=1 LZ4_SUPPORT=1 ZSTD_SUPPORT=1 \
%make_build -C squashfs-tools

}

install() {
install -D -m 755 squashfs-tools/mksquashfs %{buildroot}%{_sbindir}/mksquashfs
install -D -m 755 squashfs-tools/unsquashfs %{buildroot}%{_sbindir}/unsquashfs

}

