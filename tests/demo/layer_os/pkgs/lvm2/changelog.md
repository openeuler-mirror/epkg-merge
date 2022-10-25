* Sat Oct 15 2022 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.16-1
- upgrade version to 2.03.16

* Tue Oct 11 2022 miaoguanqin <miaoguanqin@huawei.com> - 8:2.03.14-7
- lvm: remove no locking warning

* Sun Sep 04 2022 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.14-6
- lvm: fix segfault of pvscan --cache

* Wed Apr 27 2022 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.14-5
- lvm: fix error of epoch version

* Sun Jan 30 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 8:2.03.14-4
- lvm: code reduce cyclomatic complexity

* Sun Jan 30 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 8:2.03.14-3
- dev_name() determine whether the dev->aliases linked list is
empty before obtaining the dev name

* Sun Jan 30 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 8:2.03.14-2
- check DM_NAME before creating symlink in 13-dm-disk.rules

* Mon Nov 22 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.14-1
- upgrade to 2.03.14

* Mon Nov 08 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-6
- add device-mapper-event to solve the problem of compilation error

* Wed Jul 28 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-5
- %check modified to make run-unit-test

* Wed Jul 28 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-4
- lvreduce support --yes option

* Mon Jul 26 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-3
- revert commit of fix VERSION issue when packaging

* Fri Jul 23 2021 zhouwenpei <zhouwenpei1@huawei.com> - 8:2.03.11-2
- remove unnecessary build require.

* Thu Jan 28 2021 wuguanghao<wuguanghao3@huawei.com> - 8:2.03.11-1
- update lvm2 version to 2.03.11

* Wed Dec 23 2020 yanglongkang <yanglongkang@huawei.com> - 8:2.03.09-5
- backport upstream patches-epoch2 to fix some problems

* Wed Nov 4 2020 lixiaokeng <lixiaokeng@huawei.com> - 8:2.03.09-4
- add make test

* Thu Aug 6 2020 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.09-3
- update master branch device-mapper-version more than LTS branch

* Fri Jul 24 2020 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.09-2
- update device-mapper-version to 1.02.151

* Tue Jul 14 2020 wuguanghao <wuguanghao3@huawei.com> - 8:2.03.09-1
- update lvm2 version to 2.03.09-1


* Thu Jul 2 2020 Wu Bo <wubo009@163.com> - 8:2.02.181-9
- rebuild package

* Fri Mar 20 2020 hy-euler <eulerstoragemt@huawei.com> - 8:2.02.181-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: the building requires the gdb

* Wed Mar 11 2020 wangjufeng <wangjufeng@huawei.com> - 8:2.02.181-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix heap memory leak

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix VERSION issue when packaging

* Sat Dec 28 2019 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync bugfix from community

* Mon Dec 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync bugfix from community

* Sat Nov 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-3
- Type:NA
- ID:NA
- SUG:NA
- DESC:remove some buildrequires in spec

* Fri Sep 06 2019 openEuler Buildteam <buildteam@openeuler.org> - 8:2.02.181-2
- Package init
