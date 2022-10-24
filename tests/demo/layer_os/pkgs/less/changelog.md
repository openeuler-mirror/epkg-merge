* Thu Oct 13 2022 fuanan <fuanan3@h-partners.com> - 590-2
- DESC:fix the changelog exception macro

* Fri Sep 24 2021 fuanan <fuanan3@huawei.com> - 590-1
- update version to 590

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 563-3
- DESC: delete -S git from autosetup, and delete BuildRequires git

* Fri May 28 2021 fuanan <fuanan3@huawei.com> - 563-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:[add] backport patches from upstream
Create only one ifile when a file is opened under different names.
Remove extraneous frees, associated with removed call to lrealpath.
Fix crash when call set_ifilename with a pointer to the name that is
Remove unnecessary call to pshift in pappend.
Reset horizontal shift when opening a new file.
Protect from buffer overrun.
Make histpattern return negative value to indicate error.
Lesskey: don't translate ctrl-K in an EXTRA string.
Ignore SIGTSTP in secure mode.
Fix "Tag not found" error while looking for a tag's location
Fix minor memory leak with input preprocessor.

* Thu Jan 21 2021 wangchen <wangchen137@huawei.com> - 563-1
- Update to 563

* Thu Jan 09 2020 openEuler Buildteam <buildteam@openeuler.org> - 551-3
- Delete unneeded files

* Fri Sep 27 2019 yefei <yefei25@huawei.com> - 551-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: delete irrelevant comment

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 551-1
- Package Init
