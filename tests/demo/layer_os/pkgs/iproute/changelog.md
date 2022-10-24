* Mon Oct 10 2022 jiangheng<jiangheng14@huawei.com> - 5.15.0-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:bridge: fix memory leak when doing fdb get
mptcp: fix memory leak when doing 'endpoint show'
mptcp: fix memory leak when getting limits
ip neigh: fix memory leak when doing 'get'
ip address: fix memory leak when specifying device
fix marco expansion in changelog

* Fri Aug 26 2022 sunsuwan<sunsuwan3@huawei.com> - 5.15.0-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:lnstat: fix buffer overflow in header output
libnetlink: fix socket leak in rtnl_open_byptoyo
lnstat: fix strdup leak in w argument parsing
q_cake: allow fix buffer overflow on large labels
tc flower: fix buffer overflow on large labels
tc_tuil: fix parsing action control with space and sl
tipc: fix keylen check
fix devlink health dump command without arg
tc: em_u32: fix offset parsing
l2tp fix typo in AF_INET6 checksum JSON print
ip: Fix size_columns() for very large values
ip: Fix size_columns() invocation that passes a 32-bit quantity

* Tue Mar 01 2022 jiangheng<jiangheng12@huawei.com> - 5.15.0-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: remove libcap-devel dependency

* Mon Feb 21 2022 jiangheng<jiangheng12@huawei.com> - 5.15.0-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: remove libdb-devel dependency

* Fri Nov 26 2021 jiangheng <jiangheng12@huawei.com> - 5.15.0-1
- DESC: update to 5.15.0

* Mon Aug 02 2021 chenyanpanHW <chenyanpan@huawei.com> - 5.10.0-2
- DESC: delete -S git from autosetup, and delete BuildRequires git

* Tue Jan 26 2021 xihaochen<xihaochen@huawei.com> - 5.10.0-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC: update iproute to 5.10.0

* Thu Dec 10 2020 zhouyihang <zhouyihang3@huawei.com> - 5.7.0-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:modify fix of get_tc_lib err

* Thu Sep 24 2020 zhouyihang <zhouyihang3@huawei.com> - 5.7.0-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix get_tc_lib err

* Wed Jul 22 2020 hanzhijun <hanzhijun1@huawei.com> - 5.7.0-1
- update to 5.7.0

* Mon Jan 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.4.0-2
- fix maddr show and change proc to ipnetnsproc

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.4.0-1
- update to 5.4.0

* Fri Oct 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.2.0-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add the bugfix about iproute

* Thu Sep 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 5.2.0-1
- Package init
