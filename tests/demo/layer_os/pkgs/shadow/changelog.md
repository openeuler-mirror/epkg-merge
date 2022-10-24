* Tue Aug 2 2022 zhengxiaoxiao <zhengxiaoxiao2@huawei.com> - 2:4.9-4
- add-sm3-crypt-support.patch add update release to 4.9-4

* Mon Feb 21 2022 panxiaohe <panxh.life@foxmail.com> - 2:4.9-1
- update to 4.9
- synchronized login.defs with upstream file
- useradd: modify check ID range for system users

* Thu Sep 30 2021 steven Y.Gui <steven_ygui@163.com> - 2:4.8.1-7
- backport some patches to fix memory leak

* Mon Jul 26 2021 wangchen<wangchen137@huawei.com> - 2:4.8.1-6
- delete unnecessary gdb from BuildRequires

* Thu Apr 29 2021 Hugel<gengqihu1@huawei.com> - 2:4.8.1-5
- shadow should depend on audit-libs

* Thu Jul 9 2020 Anakin Zhang<benjamin93@163.com> - 2:4.8.1-4
- fix zh_CN typo

* Sun Jun 28 2020 Anakin Zhang<benjamin93@163.com> - 2:4.8.1-3
- generate /var/spool/mail/$USER with the proper SELinux user identity

* Tue May 12 2020 steven<steven_ygui@163.com> - 2:4.8.1-2
- Enable --with-libpam config during compiling

* Fri Apr 24 2020 steven<steven_ygui@163.com> - 2:4.8.1-1
- Upgrade version to 4.8.1

* Sat Mar 21 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-10
- Only package man file into shadow-help; add buildrequires of gdb

* Tue Mar 17 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-9
- Remove redundant file

* Fri Feb 21 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-8
- Remove redundant patches

* Thu Feb 6 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-7
- User name can start with an upper case letter

* Sat Jan 18 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-6
- Delete ALWAYS_SET_PATH, which has been set by security-tool

* Thu Jan 16 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-5
- Fix unknown item 'LASTLOG_MAX_UID'

* Sun Jan 12 2020 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-4
- Delete unused patch

* Thu Dec 19 2019 openEuler Buildteam <buildteam@openEuler.org> - 2:4.7-3
- Delete unused infomation

* Mon Dec 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 2:4.7-2
- fix invaild path

* Thu Aug 29 2019 hexiaowen <hexiaowen@huawei.com> - 2:4.7-1
- update to 4.7

* Tue Aug 20 2019 guoxiaoqi<guoxiaoqi2@huawei.com> - 2:4.6-2.h9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:rename patches

* Thu Aug 8 2019 guoxiaoqi <guoxiaoqi2@huawei.com> - 2:4.6-2.h8
- Type:NA
- ID:NA
- SUG:NA
- DESC: format patches

* Thu Aug 1 2019 Jiangchuangang<Jiangchuangang@huawei.com> - 2:4.6-2.h7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:openEuler Debranding

* Fri May 3 2019 lubing<lubing6@huawei.com> - 2:4.6-2.h6
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix lock file residue

* Tue Mar 12 2019 yangzhuangzhuang<yangzhuangzhuang1@huawei.com> - 2:4.6-2.h5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:su.c: run pam_getenvlist() after setup_env
Log UID in nologin
Fix some issues found in Coverity scan.
useradd: fix segfault trying to overwrite const data with mkstemp
Fix the default mentioned in man page for SUB_UID/GID_COUNT variables.

* Wed Mar 6 2019 hanzhijun<hanzhijun@huawei.com> - 2:4.6-2.h4
- Type:bugfix
- ID:NA
- SUG:NA
DESC:shadow 4.1.5.1 var lock

* Thu Jan 31 2019 liuqianya<liuqianya@huawei.com> - 2:4.6-2.h3
- Type:bugfix
- ID:NA
- SUG:NA
DESC:Revert"shadow 4.1.5.1 var lock"

* Mon Jan 28 2019 liuqianya<liuqianya@huawei.com> - 2:4.6-2.h2
- Type:bugfix
- ID:NA
- SUG:NA
DESC:Revert "shadow-utils: sync patches"

* Fri Jan 25 2019 liuqianya<liuqianya@huawei.com> - 2:4.6-2.h1
- Type:bugfix
- ID:NA
- SUG:NA
DESC:add ruserok to avoid compilation failure
hulk shadow remove passwd param for useradd
shadow 4.1.5.1 var lock

* Sat Jul 14 2018 Jiangchuangang<Jiangchuangang@huawei.com> - 2:4.6-2
- Package Initialization
