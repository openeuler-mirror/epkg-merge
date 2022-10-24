Name:     squashfs-tools
Version:  4.5.1
Release:  1
Summary:  Utility for the squashfs filesystems
License:  GPLv2+
URL:      http://squashfs.sourceforge.net/

Source0:  http://downloads.sourceforge.net/squashfs/squashfs-tools-%{version}.tar.gz

BuildRequires: zlib-devel xz-devel libzstd-devel 
BuildRequires: lzo-devel libattr-devel lz4-devel gcc

%description
Squashfs is a highly compressed read-only filesystem for Linux.
It uses either gzip/xz/lzo/lz4/zstd compression to compress both files, inodes
and directories.

%prep
%autosetup -n squashfs-tools-%{version} -p1

%build
CFLAGS="%{optflags}" XZ_SUPPORT=1 LZO_SUPPORT=1 LZMA_XZ_SUPPORT=1 LZ4_SUPPORT=1 ZSTD_SUPPORT=1 \
%make_build -C squashfs-tools

%install
install -D -m 755 squashfs-tools/mksquashfs %{buildroot}%{_sbindir}/mksquashfs
install -D -m 755 squashfs-tools/unsquashfs %{buildroot}%{_sbindir}/unsquashfs

%files
%defattr(-,root,root)
%doc ACKNOWLEDGEMENTS README-4.5.1
%license COPYING
%{_sbindir}/mksquashfs
%{_sbindir}/unsquashfs



%changelog
* Sat Aug 13 2022 volcanodragon <linfeilong@huawei.com> - 4.5.1-1
- update version to 4.5.1

* Thu Nov 25 2021 yanglongkang <yanglongkang@huawei.com> - 4.5-1
- update to 4.5

* Tue Nov 9 2021 yanglongkang <yanglongkang@huawei.com> - 4.4-5
- Fix CVE-2021-41053 CVE-2021-41072

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 4.4-4
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Tue Jun 29 2021 zhouwenpei <zhouwenpei1@huawei.com> - 4.4-3
- add buildrequire gcc.

* Mon Jul 13 2020 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 4.4-2
- backport upstream bugfix patches

* Tue Oct 15 2019 zhanghaibo <ted.zhang@huawei.com> - 4.4-1
- Rebase to version 4.4

* Wed Jul 18 2018 openEuler Buildteam <buildteam@openeuler.org> - 4.3-17
- Package init
