* Tue Sep 6 2022 zhanchengbin <zhanchengbin1@huawei.com> - 2:2.5.4-8
- nfs-blkmapd: Fix the error status when nfs-blkmapd stops

* Thu Aug 11 2022 xueyamao <xueyamao@ktlinos.cn> - 2:2.5.4-7
- systemd: Fix format-overflow warning.

* Sat Apr 16 2022 Wu Bo <wubo40@huawei.com> - 2.5.4-6
- Update epoch version to 2. In order to fix the upgrade issues.

* Fri Apr 8 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 2.5.4-5
- set use-gss-proxy to true in nfs.conf to be consistent with the
description of 0002-nfs-utils-set-use-gss-proxy-1-to-enable-gss-proxy-by.patch

* Mon Mar 7 2022 yanglongkang <yanglongkang@h-partners.com> - 2.5.4-4
- fix nfs-blkmapd service core dump

* Thu Feb 24 2022 Wu Bo <wubo40@huawei.com> - 2.5.4-3
- idmapd Fix error status when nfs idmapd exits

* Sat Jan 29 2022 Zhiqiang Liu <liuzhiqiang26@huawei.com> - 2.5.4-2
- In order to be consistent with the old versions, here we set
use-gss-proxy to true in nfs.conf.

* Thu Nov 18 2021 Wenchao Hao <haowenchao@huawei.com> - 2.5.4-1
- update nfs-utils version to 2.5.4-1

* Thu Dec 17 2020 yanglongkang <yanglongkang@huawei.com> - 2.5.1-2
- set help package as install requires

* Thu Jul 16 2020 wuguanghao <wuguanghao3@huawei.com> - 2.5.1-1
- update nfs-utils version to 2.5.1-1

* Tue Jun 30 2020 volcanodragon <linfeilong@huawei.com> - 2.4.2-4
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:rename patch

* Sat Mar 28 2020 hy <eulerstoragemt@huawei.com> - 2.4.2-3
- Type:enhancemnet
- ID:NA
- SUG:restart
- DESC:add make check

* Fri Jan 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.2-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:stop the var-lib-nfs-rpc_pipefs.mount before remove the package

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.4.2-1
- Type:enhancemnet
- ID:NA
- SUG:NA
- DESC:update the package from 2.3.3 version to 2.4.2

* Sun Dec 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.3.3-5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:Modify the wrong service file name in spec file

* Sun Sep 29 2019 zhanghaibo <ted.zhang@huawei.com> - 2.3.3-4
- Remove some comments

* Thu Sep 05 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.3.3-3
- Package init
