* Mon Aug 15 2022 laokz <laokz@foxmail.com> - 11.1-4
- fix riscv64 relevant config

* Fri Jul  8 2022 cenhuilin <cenhuilin@kylinos.cn> - 11.1-3
- set entry point when text segment is missing

* Tue Apr 12 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 11.1-2
- fix gdb build error via cherry-pick upstream patch

* Wed Dec 8 2021 zhouwenpei <zhouwenpei1@huawei.com> - 11.1-1
- upgrade GDB version to 11.1

* Fri Aug 13 2021 zhouwenpei <zhouwenpei1@huawei.com> - 9.2-7
- adjust include order to avoid gnulib error

* Fri Jul 23 2021 zhouwenpei <zhouwenpei1@huawei.com> - 9.2-6
- remove unnecessary build require.

* Mon Apr 19 2021 yuxiangyang <yuxiangyang4@huawei.com> - 9.2-5
- remove unnecessary build require.

* Mon Apr 19 2021 yuxiangyang <yuxiangyang4@huawei.com> - 9.2-5
- remove unnecessary build require.

* Wed Mar 31 2021 xinghe <xinghe1@huawei.com> - 9.2-4
- fix typo for name

* Sat Nov 7 2020 Qingqing Li<liqingqing3@huawei.com> - 9.2-3
- cause riscv64 do not support gdbserver, create a empty package for it.
- add -fPIC option.

* Sun Sep 13 2020 licihua<licihua@huawei.com> - 9.2-2
- Change the sequence of patch and sources

* Wed Jul 22 2020 qinyu<qinyu16@huawei.com> - 9.2-1
- upgrade GDB version to 9.2

* Wed Apr  8 2020 Yunfeng Ye<yeyunfeng@huawei.com> - 8.3.1-12
- remove some useless information for cleancode

* Wed Mar 11 2020 yuxiangyang<yuxiangyang4@huawei.com> - 8.3.1-11
- backport upstream patch to fix hang in stop_all_stop

* Mon Feb  3 2020 yuxiangyang<yuxiangyang4@huawei.com> - 8.3.1-10
- fix CVE-2017-9778

* Thu Jan 16 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.3.1-9
- rpm upgrade successful, delete the dependence to librpm8

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.3.1-8
- add build requirement librpm8

* Wed Jan  8 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.3.1-7
- Upgrade GDB version to 8.3.1

* Tue Dec 24 2019 yuxiangyang<yuxiangyang4@huawei.com> - 8.2-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: Modify the requirement about python2/3 when compilation rpm.

* Thu Dec 19 2019 yeyunfeng<yeyunfeng@huawei.com> - 8.2-5
- Type:cves
- ID:CVE-2017-9778
- SUG:NA
- DESC: fix CVE-2017-9778

* Wed Sep 11 2019 openEuler Buildteam <buildteam@openeuler.org> - 8.2-4
- Package init
