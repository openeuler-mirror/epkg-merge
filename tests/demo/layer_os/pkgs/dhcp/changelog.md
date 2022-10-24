* Mon Oct 17 2022 renmingshuai <renmingshuai@huawei.com> - 12:4.4.2-15
- Type:cves
- ID:CVE-2022-2928,CVE-2022-2929
- SUG:restart
- DESC:Fix CVE-2022-2928 and CVE-2022-2929

* Tue Sep 27 2022 renmingshuai <renmingshuai@huawei.com> - 12:4.4.2-14
- Type:cves
- ID:CVE-2021-25214, CVE-2021-25215, CVE-2021-25219, CVE-2021-25220
- SUG:restart
- DESC:Fix CVE-2021-25214 CVE-2021-25215 CVE-2021-25219 CVE-2021-25220

* Sat Jul 30 2022 renmingshuai <renmingshuai@huawei.com> - 4.4.2-13
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:add dhX.conf.example in doc

* Tue Feb 22 2022 zengwefeng <zwfeng@huawei.com> - 4.4.2-12
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix error message display

* Wed Jan 12 2022 renmingshuai <renmingshuai@huawei.com> - 4.4.2-11
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:rename upstream patches and add reference

* Fri Jan 07 2022 renmingshuai <renmingshuai@huawei.com> - 4.4.2-10
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:remove buildrequires bind-export-devel and buildin bind

* Fri Nov 26 2021 renmingshuai <renmingshuai@huawei.com> - 4.4.2-9
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix coredump when client active is NULL, add lease time config ipv6 and add a unittest

* Tue Sep 14 2021 panchenbo<panchenbo@uniontech.com.com> - 4.4.2-8
- DESC: install dhcpd.conf.example

* Fri Jul 30 2021 renmingshuai <renmingshuai@huawei.com> - 4.4.2-7
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix multiple defination with gcc 10

* Mon May 31 2021 renmingshuai <renmingshuai@huawei.com> - 4.4.2-6
- Type:CVE
- ID:NA
- SUG:restart
- DESC:CVE-2021-25217

* Sat Feb 20 2021 hanzhijun <hanzhijun1@huawei.com> - 4.4.2-5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:dhcp remove buildin bind

* Tue Dec 29 2020 quanhongfei <quanhongfei@huawei.com> - 4.4.2-4
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix dhcp 64_bit lease parse

* Thu Sep 10 2020 gaihuiying <gaihuiying1@huawei.com> - 4.4.2-3
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: change ownership of /var/lib/dhcpd/ to dhcpd:dhcpd

* Tue Sep 01 2020 yuboyun <yuboyun@huawei.com> - 4.4.2-2
- Type:NA
- ID:NA
- SUG:NA
- DESC: add yaml file

* Wed Jul 22 2020 gaihuiying<gaihuiying1@huawei.com> - 4.4.2-1
- Type:requirement
- ID:NA
- SUG:restart
- DESC: update to 4.4.2

* Tue Mar 3 2020 zhanglu<zhanglu37@huawei.com> - 4.3.6-37
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: recheck if last pid was held by other process

* Thu Feb 27 2020 zhanglu<zhanglu37@huawei.com> - 4.3.6-36
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: check if last pid when held by other process

* Wed Jan 22 2020 zhanglu<zhanglu37@huawei.com> - 4.3.6-35
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: modify dhcpd coredump when discover interfaces

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-34
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: delete patches

* Tue Dec 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-33
- rename doc subpackage as help subpackage

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-32
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix dhcpd 2038 problem;
Adds address prefix len to dhclient cli

* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-31
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: reducing getifaddrs calls and improving code performance

* Mon Sep 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 4.3.6-30
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:Fix dhcp package installation failed

* Thu Sep 5 2019 hufeng <solar.hu@huawei.com> - 4.3.6-29
-Create dhcp spec
