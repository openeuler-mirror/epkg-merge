* Mon Sep 5 2022 hanhuihui <hanhuihui5@huawei.com> - 2.72.2-3
- replace pcre1 with pcre2

* Sat Jun 18 2022 zhujunhao <zhujunhao11@huawei.com> - 2.72.2-2
- remove gnutls require

* Mon Jun 6 2022 lin zhang <lin.zhang@turbolinux.com.cn> - 2.72.2-1
- Update to 2.72.2

* Thu Jun 2 2022 lin zhang <lin.zhang@turbolinux.com.cn> - 2.72.0-1
- Update to 2.72.0

* Thu Apr 28 2022 yanan <yanan@huawei.com> - 2.68.1-12
- Type:bugfix
- DESC:fix issues found by svace static code analyzer
fix segfault,memory leak,EOF,arguments leak

* Wed Apr 6 2022 hanhui <hanhui15@h-partners.com> - 2.68.1-11
- DESC:fix gfileenumerator/gdbusobjectmanagerservice/gdbusauth of memory leak

* Fri Mar 11 2022 weijin deng <weijin.deng@turbolinux.com.cn> - 2.68.1-10
- Type:bugfix
- DESC:solve glib2 enable "glib2_debug" option causes gnome-calendar reopen
coredumped in gtk3's _gtk_widget_get_toplevel()

* Wed Mar 9 2022 yangcheng<yangcheng87@h-partners.com> - 2.68.1-9
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:remove gdbus-peer rpath compile option

* Wed Mar 2 2022 hanhui<hanhui15@h-partners.com> - 2.68.1-8
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:custom installation depend on sysprof

* Sat Feb 19 2022 wangkerong<wangkerong@h-partners.com> - 2.68.1-7
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add i686 options，fix build failure on i686

* Sun Nov 14 2021 fengtao<fengtao40@huawei.com> - 2.68.1-6
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add require gdb-headless for devel


* Tue Sep 14 2021 yangcheng<yangcheng87@huawei.com> - 2.68.1-5
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:Drop dependebcy on gamin

* Tue Sep 7 2021 fengtao<fengtao40@huawei.com> - 2.68.1-4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:enable all tests

* Sat Aug 14 2021 liuyumeng<liuyumeng5@huawei.com> - 2.68.1-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix a memory leak

* Tue Aug 10 2021 liuyumeng<liuyumeng5@huawei.com> - 2.68.1-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix the third parameter of clise-range

* Wed Jun 30 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 2.68.1-1
- Upgrade to 2.68.1 because gnome-builder and more new gnome applications
need function g_memdup2 which needs glib2 ≥2.67.3 to instead of g_memdup

* Wed May 19 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 2.66.8-1
- Upgrade to 2.66.8
- Update Version, Release
- Delete patch files, delete gio-launch-desktop(not exist in 2.66.8)
- Correct date, make it match weekday

* Tue Apr 13 2021 hanhui<hanhui15@huawei.com> - 2.62.5-5
- Type:cve
- Id:CVE-2021-28153
- SUG:NA
- DESC:fix CVE-2021-28153

* Sat Mar 6 2021 hanhui<hanhui15@huawei.com> - 2.62.5-4
- Type:cve
- Id:CVE-2021-27219
- SUG:NA
- DESC:fix CVE-2021-27219

* Mon Mar 1 2021 jinzhimin<jinzhimin2@huawei.com> - 2.62.5-3
- Type:cve
- Id:CVE-2021-27218
- SUG:NA
- DESC:fix CVE-2021-27218

* Sat Feb 27 2021 zhujunhao<zhujunhao8@huawei.com> - 2.62.5-2
- Type:cve
- Id:CVE-2020-35457
- SUG:NA
- DESC:fix CVE-2020-35457

* Tue Jul 21 2020 hanhui<hanhui15@huawei.com> - 2.62.5-1
- Update to 2.62.5

* Mon Mar 2 2020 hexiujun<hexiujun1@huawei.com> - 2.62.1-4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix accidentally delete temp file within dtrace

* Fri Feb 28 2020 zhangrui <zhangrui182@huawei.com> - 2.62.1-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:remove dist in spec

* Mon Feb 24 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.62.1-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:exclude some unnecessary files

* Thu Jan 9 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.62.1-1
- update to 2.62.1

* Tue Dec 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.58.1-6
- change the path of files

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.58.1-5
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:Fix a leaking GRemoteActionGroup member

* Sat Nov 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.58.1-4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add the libxslt in buildrequires

* Wed Sep 25 2019 huzunhao<huzunhao2@huawei.com> - 2.58.1-3
- Type:cves
- ID:CVE-2019-12450 CVE-2019-13012
- SUG:restart
- DESC:fix CVE-2019-12450 CVE-2019-13012

* Thu Sep 19 2019 Lijin Yang <yanglijin@huawei.com> - 2.58.1-2
- Package init
