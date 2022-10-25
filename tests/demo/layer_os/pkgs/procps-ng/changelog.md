* Sat Jan 29 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 3.3.17-2
- fix file type chamges caused by top -b redirection

* Thu Dec 2 2021 zhouwenpei <zhouwenpei1@huawei.com> - 3.3.17-1
- update to 3.3.17

* Wed Jun 30 2021 hewenliang <hewenliang4@huawei.com> - 3.3.16-16
- sync patches

* Sat Feb 27 2021 hewenliang <hewenliang4@huawei.com> - 3.3.16-15
- sync patches

* Sat Feb 27 2021 hewenliang <hewenliang4@huawei.com> - 3.3.16-14
- sync patches

* Tue Nov 03 2020 xinghe <xinghe1@huawei.com> - 3.3.16-13
- sync patchs

* Wed Sep 23 2020 MarsChan <chenmingmin@huawei.com> - 3.3.16-12
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:A kernel change means we cannot trust what sysconf(SC_ARG_MAX)
returns. We clamp it so its more than 4096 and less than 128*1024
which is what findutils does.

* Tue Jan 7 2020 MarsChan <chenmingmin@huawei.com> - 3.3.16-11
- Type:upgrade
- ID:NA
- SUG:NA
- DESC: upgrade to version 3.3.16 and delete the patch between
3.3.15 and 3.3.16.

* Mon Dec 23 2019 wangshuo <wangshuo47@huawei.com> - 3.3.15-10
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: add liscense to main and devel package.

* Thu Dec 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.3.15-9
- Fix typo

* Fri Mar 15 2019 xuwei<xuwei58@huawei.com> - 3.3.15-8
- Type:bugfix
- ID:NA
- SUG:restart
- DEC:top: don't mess with groff line length in man document
top: add another field sanity check in 'config_file()'
top: prevent buffer overruns in 'inspection_utility()'
docs: Tidying of ps,kill and skill manpages
library: avoid problems involving 'supgid' mishandling
w: Prevent out-of-bounds reads in
w: Clamp maxcmd to the MIN/MAX_CMD_WIDTH range.
vmstat: getopt*() returns -1 when done, not EOF.
vmstat: Replace memcmp() with strncmp().
vmstat: Check return values of localtime() and
vmstat: Prevent out-of-bounds writes in new_header()
top: the '#define PRETEND2_5_X' was found to be broken
procio: use the user-supplied delimiter to split large
procio: fix potential out-of-bounds access when write
sysctl: do not report set key in case `close_stream`

* Tue Jan 29 2019 huangchangyu<huangchangyu@huawei.com> - 3.3.15-7
- Type:bugfix
- ID:NA
- SUG:NA
- DEC:sync patches

* Wed Jan 23 2019 xuchunmei<xuchunmei@huawei.com> - 3.3.15-6
- Type:bugfix
- ID:NA
- SUG:restart
- DEC:top exit with error when pid overflow

* Fri Jan 11 2019 xuchunmei<xuchunmei@huawei.com> - 3.3.15-5
- Type:feature
- ID:NA
- SUG:restart
- DEC:add options -M and -N for top

* Sat Jul 18 2018 openEuler Buildteam <buildteam@openeuler.org> - 3.3.15-4
- Package init
