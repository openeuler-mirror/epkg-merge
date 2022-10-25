* Mon Oct 10 2022 huangduirong <huangduirong@huawei.com> - 8.2110.0-11
- Type:NA
- ID:NA
- SUG:NA
- DESC:remove the sphinx-build in prep

* Thu Aug 04 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 8.2110.0-10
- backport patches from upstream and enable check

* Mon May 23 2022 zhanghaolian <zhanghaolian@huawei.com> - 8.2110.0-9
- fix CVE-2022-24903

* Fri Mar 25 2022 wuchaochao <cyanrose@yeah.net> - 8.2110.0-8
- add systemd_lived macro

* Mon Mar 14 2022 wuchaochao <wuchaochao4@huawei.com> - 8.2110.0-7
- change startlimitburst spelling errors

* Feb Mon 28 2022  wangkerong <wangkerong@h-partners.com> - 8.2110.0-6
- Increase the limit on restart frequency

* Feb Mon 28 2022  wangkerong <wangkerong@h-partners.com> - 8.2110.0-5
- update timezone when restart rsyslog

* Wed Feb 23 2022  wuchaochao <wuchaochao4@huawei.com> - 8.2110.0-4
- delete  rsyslog-8.24.0-set-permission-of-syslogd-dot-pid-to-0644.patch

* Sat Feb 19 2022 liuyumeng <liuyumeng5@h-partners.com> - 8.2110.0-3
- print main queue info to journal

* Tue Dec 14 2021 wuchaochao <wuchaochao4@huawei.com> - 8.2110.0-2
- move rsyslog-crypto rsyslog-doc rsyslog-elasticsearch rsyslog-mmjsonparse syslog-mmaudit rsyslog-mmsnmptrapd rsyslog-mysql syslog-gssapi rsyslog-gnutls rsyslog-updspoof from rsyslog

* Thu Dec 09 2021 wuchaochao <wuchaochao4@huawei.com> - 8.2110.0-1
- update version to 8.2110.0

* Thu Aug 26 2021 wuchaochao <wuchaochao4@huawei.com> - 8.2012.0-4
- Type:NA
- ID:NA
- SUG:restart
- DESC:remove RSYSLOG_OPTIONS and change rsyslog.service files

* Wed Aug 25 2021 wuchaochao <wuchaochao4@huawei.com> - 8.2012.0-3
- Type:NA
- ID:NA
- SUG:restart
- DESC:add RSYSLOG_OPTIONS and organize rsyslog.service files

* Fri Jun 11 2021 shangyibin<shangyibin1@huawei.com> - 8.2012.0-2
- Type:NA
- ID:NA
- SUG:restart
- DESC:remove the dependence on libdbi

* Wed Feb 3 2021 yuanxin <yuanxin24@huawei.com> - 8.2012.0-1
- Upgrade version to 8.2012.0

* Thu Sep 15 2020 Guodong Zhu<zhuguodong8@huawei.com> - 8.2006.0-2
- Type:NA
- ID:NA
- SUG:restart
- DESC: fix potential file descriptor leak in one backport patch

* Mon Jul 27 2020 shixuantong<shixuantong@huawei.com> - 8.2006.0-1
- Type:NA
- ID:NA
- SUG:NA
- DESC:update to 8.2006-1

* Thu Apr 16 2020 Shouping Wang<wangshouping@huawei.com> - 8.2002.0-1
- Type: bugfix
- ID:NA
- SUG:restart
- DESC: upgrade rsyslog to 8.2002.0

* Wed Mar 25 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: the return value judgment of recv() is err in CheckConnection

* Tue Mar 24 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h4
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: parameter streamdriver.permitexpiredcerts did not work

* Thu Mar 19 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h3
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: del imjournalRatelimitInterval and add *.emerg

* Sat Mar 7 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h2
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:emergency messages not to everyone

* Fri Mar 6 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h1
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:create pid file

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.1907.0-5
- del unuse info

* Wed Nov 27 2019 chengquan <chengquan3@huawei.com> - 8.1907.0-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove useless install dependencies

* Fri Nov 8 2019 chengquan <chengquan3@huawei.com> - 8.1907.0-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add self-study patches

* Fri Oct 18 2019 chengquan <chengquan3@huawei.com> - 8.1907.0-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix spec rule in openeuler

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 8.1907.0-1
- Package init
