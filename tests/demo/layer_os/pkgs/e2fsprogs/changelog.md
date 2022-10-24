* Fri Oct 14 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 1.46.4-16
- tune2fs: fix segfault problem

* Fri Sep 23 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-15
- test: fix ACL-printing tests from community

* Sat Aug 20 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 1.46.4-14
- debugfs: teach logdump the -n <num_trans> option

* Fri Aug 12 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-13
- tune2fs: do not change j_tail_sequence in journal superblock

* Fri Jun 24 2022 wuzx<wuzx1226@qq.com> - 1.46.4-12
- add sw64 patch

* Tue Jun 21 2022 lihaoxiang <lihaoxiang9@huawei.com> - 1.46.4-11
- DESC:add wrapper header file for i686 and x86_64 then fix conflicts when intall i686 rpms.

* Sat May 28 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 1.46.4-10
- fix CVE-2022-1304

* Fri May 20 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-9
- e2fsck: handle->level is overflow in ext2fs_extent_get.

* Wed May 18 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-8
- e2fsck: do not clean up file acl if the inode is truncating type

* Thu Mar 17 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-7
- tests: skip m_rootdir_acl if selinux is not disabled

* Wed Mar 9 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-6
- libext2fs: don't old the CACHE_MTX while doing I/O

* Tue Mar 8 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-5
- tests: update expect file for u_direct_io

* Wed Mar 2 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-4
- e2mmpstatus.8.in: detele filesystem can be UUID or LABEL in manpage

* Thu Feb 24 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-3
- adapt patchs from openEuler-20.03-LTS

* Thu Jan 27 2022 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-2
- replace License in spec

* Sat Nov 27 2021 zhanchengbin <zhanchengbin1@huawei.com> - 1.46.4-1
- update package to v1.46.4.

* Mon Nov 15 2021 zhanchengbin <zhanchengbin1@huawei.com> - 1.45.6-7
- DESC: integrate community patches.

* Mon Sep 13 2021 lixiaokeng <lixiaokeng@huawei.com> - 1.45.6-6
- DESC: add newer libreadline.so.8 to dlopen path

* Fri Aug 20 2021 chenyanpanHW <chenyanpan@huawei.com> - 1.45.6-5
- DESC: add necessary BuildRequires audit

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 1.45.6-4
- DESC: delete -Sgit from %autosetup, and delete BuildRequires git

* Wed Dec 16 2020 yanglongkang <yanglongkang@huawei.com> - 1.45.6-3
- Set help package as install require

* Fri Oct 30 2020 Zhiqiang Liu <lzhq28@mail.ustc.edu.cn> - 1.45.6-2
- backport upstream patches-epoch2 to fix some problems

* Wed Jul 15 2020 Zhiqiang Liu <lzhq28@mail.ustc.edu.cn> - 1.45.6-1
- rebuild package

* Wed Jul 1 2020 Wu Bo <wubo009@163.com> - 1.45.3-5
- rebuild package

* Mon Feb 3 2020 luoshijie <luoshijie1@huawei.com> - 1.45.3-4
- Type:cves
- ID:CVE-2019-5094
- SUG:restart
- DESC:backport patch to fix CVE-2019-5094.

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.45.3-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:change path to remove no used file.

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.45.3-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix local rpmbuild error.

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.45.3-1
- Type:cves
- ID:CVE-2019-5188
- SUG:restart
- DESC:backport patch to fix CVE-2019-5188.

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.45.3-0
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update package from 1.44.3 to 1.45.3.

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.44.3-8
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update spec.

* Wed Sep 18 2019 luoshijie <luoshijie1@huawei.com> - 1.44.3-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:modify spec file to follow spec rules.

* Fri Sep 6 2019 luoshijie <luoshijie1@huawei.com> - 1.44.3-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:openEuler Debranding

* Tue Aug 20 2019 luoshijie <luoshijie1@huawei.com> - 1.44.3-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:rename patch name

* Wed Jul 10 2019 zhangyujing <zhangyujing1@huawei.com> - 1.44.3-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:e2freefrag: fix memory leak in scan_online()
create_inode: fix potential memory leak in path_append()
mke2fs: fix check for absurdly large devices

* Fri Mar 15 2019 zhangyujing <zhangyujing1@huawei.com> - 1.44.3-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:blkid avoid FPE crash when probing a HFS superblock
AOSP e2fsdroid Fix crash with invalid command line a
e2fsck fix fd leak in reserve_stdio_fds
libext2fs fix uninitialized length in rep_strdup
tune2fs fix dereference of freed memory after journa
libe2p avoid segfault when s_nr_users is too high
e2freefrag fix free blocks count during live scan

* Wed Jan 23 2019 wangxiao <wangxiao65@huawei.com> - 1.44.3-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:disable the metadata_csum creat by mke2fs -t ext4 by default
- Package init

