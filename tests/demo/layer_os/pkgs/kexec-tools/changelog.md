* Wed Aug 24 2022 chenhaixiang <chenhaixiang3@huawei.com> - 2.0.23-8
- arm64: fix PAGE_OFFSET calc for flipped mm

* Tue Aug 23 2022 chenhaixiang <chenhaixiang3@huawei.com> - 2.0.23-7
- kdumpctl:ignore deprecated and invalid kdump config option

* Wed Aug 3 2022 chenhaixiang <chenhaixiang3@huawei.com> - 2.0.23-6
- fix CVE-2021-20269

* Fri Mar 11 2022 wangbin <wangbin224@huawei.com> - 2.0.23-5
- packing 98-kexec.rules instead of 98-kexec.rules.ppc64

* Wed Feb 23 2022 wangbin <wangbin224@huawei.com> - 2.0.23-4
- arm64/crashdump: deduce paddr of _text based on kernel code size

* Wed Feb 23 2022 snoweay <snoweay@163.com> - 2.0.23-3
- Fix conflicts between quick kexec and load-live-update with xen.

* Wed Dec 29 2021 zhouwenpei <zhouwenpei1@huawei.com> - 2.0.23-2
- modify the patch header

* Sat Dec 25 2021 zhouwenpei <zhouwenpei1@huawei.com> - 2.0.23-1
- update to 2.0.23

* Tue Jul 27 2021 zhouwenpei <zhouwenpei1@huawei.com> - 2.0.20-7
- fix build fail caused by file format not recognized

* Sat Mar 27 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.0.20-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix bug: Filed to generate the vmcore file in the ARM architecture
Fix bug: Filed to generate the vmcore-dmesg.txt file in the ARM architecture

* Mon Mar 22 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.0.20-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:support more than one crash kernel regions.
Fix bugs of unuseable quick kexec on arm64, becaues of arm64-kexec-allocate-memory-space-avoiding-reserved-regions
excluding QUICK_KEXEC memory region.

* Mon Sep 14 2020 zhangruifang2020 <zhangruifang1@huawei.com> - 2.0.20-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:sychronize git patches to enhance quality

* Thu Sep 10 2020 zhangruifang2020 <zhangruifang1@huawei.com> - 2.0.20-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix issue about iomem file that contains too many contens.As a result,the kdump service failed.

* Thu Aug 13 2020 snoweay <snoweay@163.com> - 2.0.20-2
- Add support for quick kexec
kexec: Add quick kexec support
arm64: Quick kexec implementation for arm64

* Thu Jul 23 2020 zhangxingliang <zhangxingliang3@huawei.com> - 2.0.20-1
- Type:update
- ID:NA
- SUG:NA
- DESC:update to 2.0.20

* Thu May 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.0.17-16
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:fix kdump stuck

* Wed Jan 1 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.0.17-15
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify patch

* Tue Dec 31 2019 Jialong Chen <chenjialong@huawei.com> - 2.0.17-14
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify SECTION_SIZE_BITS to 30 and keep the same as the kernel configuration.
add executable permissions for kdump-error-handler.sh.

* Thu Dec 19 2019 chengquan <chengquan3@huawei.com> - 2.0.17-13
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add url for package

* Wed Sep 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.0-17.12
- add secure compile options and merge bugfix patches from community
xen: Avoid overlapping segments in low memory
x86: Check /proc/mounts before mtab for mounts
x86: Find mounts by FS type, not name
kexec/kexec.c: Add the missing close() for fd used for kexec_file_load()
kexec-uImage-arm64.c: Fix return value of uImage_arm64_probe()
kexec/kexec-zlib.h: Add 'is_zlib_file()' helper function
kexec/arm64: Add support for handling zlib compressed (Image.gz) image

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.0-17.11
- Package init

* Thu Aug 22 2019 Yeqing Peng<pengyeqing@huawei.com> - 2.0-17.10.h1
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: fix bugs as follows:
1.dmesg fix infinite loop if log buffer wraps around.
2.arm64 error out if kernel command line is too long.
3.fix an error that can not parse the e820 reserved region.
4.x86 fix BAD_FREE in get_efi_runtime_map().
5.fix check against 'fdt_add_subnode' return value.
6.arm64 add error handling check against return value of 'set_bootargs()'.
7.fix adding '/chosen' node for cases where it is not available in dtb
passed via --dtb option.
8.fix '/chosen' v/s 'chosen' node being passed to fdt helper functions.
9.arm64 wipe old initrd addresses when patching the DTB.
10.arm64 increase the command line buf space to 1536.
11.arm64 bugfix get the paddr of mem_section return error address.
12.arm64 support more than one crash kernel regions.
13.modify SECTIONS_SIZE_BITS to 27 for arm64.
