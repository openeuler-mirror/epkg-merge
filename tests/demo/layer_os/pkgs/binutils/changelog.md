* Sat Oct 08 2022 Chenxi Mao <chenxi.mao@suse.com> - 2.37-12
- Fix Aarch64 EFI PE section address overlap issue.

* Fri Sep 02 2022 Wei, Qiang <qiang.wei@suse.com> - 2.37-11
- Fix man page empty issue

* Thu Sep 8 2022 yinyongkang <yinyongkang@kylinos.cn> - 2.37-10
- Type:CVE
- ID:CVE-2022-38126
- SUG:NA
- DESC:Fix CVE-2022-38126

* Tue Aug 11 2022 dingguangya <dingguangya1@huawei.com> - 2.37-9
- Type:requirements
- ID:NA
- SUG:NA
- DESC:Enable Intel AVX512_FP16 instructions

* Fri Aug 05 2022 maminjie <maminjie8@163.com> - 2.37-8
- Fix preserve_dates: cannot set time

* Wed Jun 29 2022 Chenxi Mao <chenxi.mao@suse.com> - 2.37-7
- Add support for the EFI format to the AArch64 target.

* Tue Mar 15 2022 zoulin <zoulin13@h-partners.com> - 2.37-6
- Type:requirements
- ID:NA
- SUG:NA
- DESC:fix (obs) project build fail

* Sat Mar 12 2022 zoulin <zoulin13@h-partners.com> - 2.37-5
- Type:requirements
- ID:NA
- SUG:NA
- DESC:add binutils-extra

* Fri Jan 21 2022 Kai Liu <kai.liu@suse.com> - 2.37-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix upstream bug #28138, which results in "malformed archive" error when building nodejs

* Wed Jan 19 2022 panxiaohe <panxiaohe@huawei.com> - 2.37-3
- Type:CVE
- ID:CVE-2021-42574
- SUG:NA
- DESC:Fix CVE-2021-42574

* Fri Dec 24 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.37-2
- Type:CVE
- ID:CVE-2021-45078
- SUG:NA
- DESC:Fix CVE-2021-45078

* Thu Dec 2 2021 wangchen <wangchen137@huawei.com> - 2.37-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC:update to 2.37

* Tue Sep 14 2021 panxiaohe <panxiaohe@huawei.com> - 2.36.1-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: fix issue about delete symlink when using the strip command

* Tue Sep 7 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.36.1-2
- Type:requirements
- ID:NA
- SUG:NA
- DESC:remove rpath and runpath of exec files and libraries

* Mon Jul 5 2021 yixiangzhike <zhangxingliang3@huawei.com> - 2.36.1-1
- Type:NA
- ID:NA
- SUG:NA
- DESC: update to 2.36.1

* Sat Jun 19 2021 wangchen <wangchen137@huawei.com> - 2.34-13
- Type:CVE
- ID:NA
- SUG:NA
- DESC: fix CVE-2021-3549

* Fri Apr 23 2021 lirui <lirui130@huawei.com> - 2.34-12
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2021-3487

* Fri Apr 16 2021 lirui <lirui130@huawei.com> - 2.34-11
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2021-20197

* Tue Mar 23 2021 panxiaohe <panxiaohe@huawei.com> - 2.34-10
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2020-0551

* Mon Mar 22 2021 lirui <lirui130@huawei.com> - 2.34-9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:move the test to %check phase

* Sat Jan 9 2021 zoulin <zoulin13@huawei.com> - 2.34-8
- Type:CVE
- ID:NA
- SUG:NA
- DESC:fix CVE-2020-16592

* Wed Nov 4 2020 Qingqing Li <liqingqing3@huawei.com> - 2.34-7
- Type:bugfix
- ID:NA
- SUG:fully support for riscv64.

* Tue Nov 3 2020 Qingqing Li <liqingqing3@huawei.com> - 2.34-6
- Type:bugfix
- ID:NA
- SUG:riscv64 do not support gold linker, add a condition to distinguish it.

* Sat Oct 31 2020 Qingqing Li <liqingqing3@huawei.com> - 2.34-5
- Type:bugfix
- ID:NA
- SUG:fix changelog date.

* Fri Sep 18 2020 zoulin <zoulin13@huawei.com> - 2.34-4
- Type:bugfix
- ID:NA
- SUG:Fix a potential use-of-an-uninitialised-value in the print_insn_ns32k of fuzz_disassemble

* Fri Sep 11 2020 zoulin <zoulin13@huawei.com> - 2.34-3
- Type:bugfix
- ID:NA
- SUG:Fix a memory leak in the testcase fuzz_readelf
Fix use-of-uninitialized-value in print_insn_mwtag
Fix use-of-ninitialized-value in _bfd_xcoff_slurp_armap

* Wed Aug 5 2020 zhangxingliang <zhangxingliang3@huawei.com> - 2.34-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix static library file conflicts when install both binutils and binutils-devel

* Fri Jul 24 2020 zhangxingliang <zhangxingliang3@huawei.com> - 2.34-1
- Type:update
- ID:NA
- SUG:NA
- DESC:update to 2.34

* Tue Jul 14 2020 linwei <linwei54@huawei.com> - 2.33.1-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix use-of-uninitialized-value in print_insn_nds32

* Fri May 15 2020 wangchen <wangchen137@huawei.com> - 2.33.1-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix memory leak in bfd_check_format

* Thu Apr 02 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Use disassemble_info.private_date in place of insn_sets

* Wed Jan 22 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-5
- Type:bugfix
- ID:CVE
- SUG:NA
- DESC: fix permission

* Mon Jan 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-4
- Type:bugfix
- ID:CVE
- SUG:NA
- DESC:fix the issue that the permission changes due to the upgrade and
backport patch to fix memory leak and overflow

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-3
- Type:bugfix
- ID:CVE
- SUG:NA
- DESC:add patch to solve complaining about relocs in the .gnu.build.attribute

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-2
- Type:bugfix
- ID:CVE
- SUG:NA
- DESC:add libbfd.so and libopcodes.so for kernel building

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.33.1-1
- Type:enhancement
- ID:CVE
- SUG:NA
- DESC:update version to 2.33.1

* Fri Dec 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.31.1-16
- Type:cves
- ID:CVE
- SUG:NA
- DESC:fix CVE-2018-20671 CVE-2019-12972 CVE-2019-17450 CVE-2019-17451
CVE-2018-18309 CVE-2018-18309 CVE-2018-18605 CVE-2018-18607 CVE-2018-18606
CVE-2018-1000876 CVE-2018-20002 CVE-2018-20002 CVE-2019-1010180
fix failure in the libiberty testsuite
fix stack-buffer-overflow, and use-of-uninitialized-value and shift exponent -1 is negative

* Mon Sep 23 2019 luhuaxin <luhuaxin@huawei.com> - 2.31.1-15
- Patch synchronization and update dependency name
- Type:cves
- ID:CVE-2019-1010204
- SUG:NA
- DESC:fix CVE-2019-1010204

* Wed Sep 04 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.31.1-14
- Package init
