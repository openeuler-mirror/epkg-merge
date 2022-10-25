Name:           dosfstools
Version:        4.2
Release:        1
Summary:        FAT file system userspace tools
License:        GPLv3+
URL:            http://www.github.com/dosfstools/dosfstools
Source0:        http://www.github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc autoconf automake

%description
The dosfstools package contains programs mkfs.fat, fsck.fat and fatlabel to
create, check and label FAT family file systems.

%package        help
Summary:        Documentations for dosfstools
BuildArch:      noarch
Requires:       man

%description    help
This package includes man pages for dosfstools.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --enable-compat-symlinks
%make_build CFLAGS="%{optflags} -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -fno-strict-aliasing"

%check
make check

%install
%make_install

%files
%doc NEWS README doc/* ChangeLog
%license COPYING
%{_sbindir}/*
%exclude %{_docdir}/%{name}/COPYING


%files help
%{_mandir}/man8/*

%changelog
* Wed Nov 17 2021 Wenchao Hao <haowenchao@huawei.com> - 4.2-1
- Update to dosfstools-4.2

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 4.1-11
- DESC: delete -S git from %autosetup, and delete BuildRequires git

* Tue Feb 9 2021 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 4.1-10
- backport patches to fix two memory leak problems, rename patch names,
  and set release num to 9 for CI.

* Wed Nov 4 2020 lixiaokeng <lixiaokeng@huawei.com> - 4.1-9
- add make check

* Wed Jul 1 2020 Wu Bo <wubo009@163.com> - 4.1-8
- rebuild package

* Tue Aug 20 2019 luoshijie <luoshijie1@huawei.com> - 4.1-7
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:openEuler Debranding

* Tue Aug 20 2019 luoshijie <luoshijie1@huawei.com> - 4.1-6.h2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:rename patch name

* Mon Apr 15 2019 yinzhiwei <yinzhiwei5@huawei.com> - 4.1-6.h1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix signed integer overflow in FSTART
       Avoid returning deleted directory entries as labels
       src check.c: Fix up mtools created bad dir entries
       Remove long file name when changing short file name
       Fix gcc sprintf length warnings
       fsck.fat: Fix Year 2038 Bug
       mkfs.fat: Fix parsing of block number
       device_info: Fix parsing partition number
-Package init

