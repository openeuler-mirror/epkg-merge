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

