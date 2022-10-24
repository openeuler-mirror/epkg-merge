* Sat Feb 12 2022 yixiangzhike <yixiangzhike007@163.com> - 3.0.1-2
- Fix failure of stopping auditd before uninstalling

* Fri Dec 31 2021 yixiangzhike <yixiangzhike007@163.com> - 3.0.1-1
- update to 3.0.1

* Tue Nov 16 2021 yixiangzhike <yixiangzhike007@163.com> - 3.0-4
- backport some patches
Turn libaucommon into a libtool convenience library
Fix the closing timing of audit_fd
Fix some string length issues
Move the free_config to success path
Check for fuzzer induced invalid value
error out if log is mangled
Dont run off the end with corrupt logs
Another hardening measure for corrupted logs
Fix busy loop in normalizer when logs are corrupt
Better fix for busy loop in normalizer when logs are corrupt
flush uid gid caches when user group added deleted modified
In auditd check if log_file is valid before closing handle
Check ctime return code
When interpreting if val is NULL return an empty string
auditd.service Restart on failure ignoring some exit
In auditd close the logging file descriptor when logging is suspended

* Wed Sep 1 2021 steven.ygui <steven_ygui@163.com> - 3.0-3
- backport some patches to fix memory leak and double free issues

* Fri May 28 2021 yixiangzhike <zhangxingliang3@huawei.com> - 3.0-2
- solve the script failure when package upgrade

* Tue May 25 2021 yixiangzhike <zhangxingliang3@huawei.com> - 3.0-1
- update to 3.0

* Mon May 24 2021 yixiangzhike <zhangxingliang3@huawei.com> - 2.8.5-4
- fix directory permissions for /etc/audisp and /etc/audisp/plugins.d

* Thu Oct 29 2020 zhangxingliang <zhangxingliang3@huawei.com> - 2.8.5-3
- remove python2 subpackage

* Wed Aug 19 2020 wangchen <wangchen137@huawei.com> - 2.8.5-2
- add epoch for requires

* Wed Jul 29 2020 wangchen <wangchen137@huawei.com> - 2.8.5-1
- revert to 2.8.5

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.0-5
- add subpackages

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.0-4
- clean code

* Wed Oct 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.0-3
- Adjust requires

* Sun Sep 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.0-2
- Fix the auditctl error

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.0-1
- Package init
