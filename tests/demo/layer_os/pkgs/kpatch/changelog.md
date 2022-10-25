* Sun Oct 9 2022 Bin Hu <hubin73@huawei.com> -1:0.9.5-15
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:create-diff-object: add support for .return_sites section

* Sun Oct 9 2022 Bin Hu <hubin73@huawei.com> -1:0.9.5-14
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:lookup: skip finding local symbols for object with no local symbols

* Tue Sep 6 2022 Tang Bin <tangbin_yewu@cmss.chinamobile.com> -1:0.9.5-13
- Type:clean code
- ID:NA
- SUG:NA
- DESC:kpatch-build: Remove duplicate functions

* Tue Sep 6 2022 Tang Bin <tangbin_yewu@cmss.chinamobile.com> -1:0.9.5-12
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:kpatch-build: fix loading error in aarch64

* Mon Sep 5 2022 Tang Bin <tangbin_yewu@cmss.chinamobile.com> -1:0.9.5-11
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:livepatch-patch-hook: fix kpatch-build error which do not support ftrace

* Mon May 30 2022 Bin Hu <hubin73@huawei.com> -1:0.9.5-10
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:make_hotpatch: fix some grammar error

* Mon May 23 2022 Bin Hu <hubin73@huawei.com> -1:0.9.5-9
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:create-diff-object: fix some hotpatch compilation problems

* Thu May 12 2022 Bin Hu <hubin73@huawei.com> -1:0.9.5-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:livepatch-patch-hook: fix HAVE_SIMPLE_ENABLE

* Tue May 10 2022 Bin Hu <hubin73@huawei.com> -1:0.9.5-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:kpatch-build: do not copy linux scripts when building OOT module hotpatch

* Tue May 10 2022 Bin Hu <hubin73@huawei.com> -1:0.9.5-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix segment fault and hotpatch compilation problem when using openEuler 22.03 LTS kernel

* Wed Mar 30 2022 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.5-5
- Type:clean code
- ID:NA
- SUG:NA
- DESC:delete useless code

* Sun Feb 6 2022 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.5-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix "ERROR: util.o: find_local_syms: 185: found duplicate matches for util.c"

* Wed Jan 26 2022 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.5-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:backport upstream patch

* Wed Dec 22 2021 Wentao Fan<fanwentao@huawei.com> -1:0.9.5-2
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:backport upstream patch

* Sat Nov 13 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.5-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:upgrade to upstream v0.9.5

* Sat Oct 30 2021 Bin Hu<hubin57@huawei.com> -1:0.9.1-21
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:backport upstream patch

* Tue Oct 26 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-20
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:backport upstream patches

* Tue Oct 26 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-19
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:support make compile environment

* Tue Sep 28 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-18
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:kpatch: update sympos for duplicate symbols in vmlinux
create-diff-object: fix segment fault when sec2->rela is NULL

* Tue Sep 28 2021 Bin Hu<hubin57@huawei.com> -1:0.9.1-17
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove uname-build-check from build dependency

* Sat Aug 21 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-16
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:create-diff-object: error on detect new/changed ALTINSTR_ENTRY_CB

* Fri Jul 23 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-15
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: lookup: Add __UNIQUE_ID_ to maybe_discarded_sym list

* Mon May 31 2021 Xinpeng Liu<liuxp11@chinatelecom.cn> -1:0.9.1-14
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify the code stype in make_hotpatch and fix compile bug

* Sat May 29 2021 Wentao Fan<fanwentao@huawei.com> -1:0.9.1-13
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:support for .cold functions with no id suffix

* Wed Feb 10 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-12
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify hotpatch id length limit from 20 to 32

* Mon Jan 11 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-11
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add kpatch requires

* Tue Jan 5 2021 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-10
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:only skip gcc check in cross compile environment

* Thu Dec 31 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-9
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:support remove static variables using KPATCH_IGNORE_STATIC

* Sun Nov 22 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix relocation not resolved when new functions exported only

* Tue Nov 17 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-7
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:optimize for out of tree module

* Thu Nov 12 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add help package Recommends

* Fri Sep 25 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update Source0

* Sat Sep 12 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:code optimization

* Sat Aug 29 2020 Yeqing Peng<pengyeqing@huawei.com> -1:0.9.1-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:adapt kernel source path and name

* Wed Apr 22 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix duplicate symbols in vmlinux

* Wed Apr 15 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -1:0.9.1-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:rebase from upstream version v0.9.1
Use Epoch to make the version number consistent with the upstream

* Thu Mar 12 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -2.0-3.1.26
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:use orignal reloc for export symbols in all modules

* Thu Mar 12 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -2.0-3.1.25
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change livepatch and os_hotpatch to permission and exclude in main package

* Wed Feb 26 2020 Zhipeng Xie<xiezhipeng1@huawei.com> -2.0-3.1.24
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:rebase from upstream version v0.9.0

* Mon Feb 17 2020 openEuler Buildteam <buildteam@openeuler.org> -2.0-3.1.23
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add subpackage kpatch-runtime

* Mon Dec 30 2019 openEuler Buildteam <buildteam@openeuler.org> -2.0-3.1.22
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change some patch name and delete useless code

* Mon Dec 23 2019 openEuler Buildteam <buildteam@openeuler.org> -2.0-3.1.21
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify email adress

* Thu Dec 19 2019 chengquan<chengquan3@huawei.com> -2.0-3.1.20
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:remove useless description

* Thu Nov 28 2019 Yufa Fang<fangyufa1@huawei.com> - 2.0-3.1.19
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix compilation with CONFIG_HAVE_ARCH_PREL32_RELOCATIONS

* Thu Oct 10 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.18
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add security compile flags

* Fri Sep 27 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.17
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:create-diff-object: allow changing subsections

* Tue Sep 24 2019 shenyangyang<shenyangyang4@huawei.com> -2.0-3.1.16
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:revise help package and subpackage

* Mon Aug 26 2019 openEuler Buildteam<buildteam@openeuler.org> -2.0-3.1.15
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:changelog some patch commit message

* Tue Aug 20 2019 openEuler Builteam <buildteam@openeuler.org> -2.0-3.1.14
- Type:NA
- ID:NA
- SUG:NA
- DESC:rewrite spec

* Tue Jul 16 2019 yangbin<robin.yb@huawei.com> - 2.0-3.1.13
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add object in kpatch

* Fri Jul 5 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.12
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix ref static local symbol for longname symbol

* Mon Jul 1 2019 Enbo Kang<kangenbo@huawei.com> - 2.0-3.1.11
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:fix security problem

* Tue May 7 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.10
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:change some patch to backport prefix

* Sat Apr 13 2019 hezhanyu<hezhanyu@huawei.com> - 2.0-3.1.9
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:modify private key in sign-modules

* Thu Apr 4 2019 Enbo Kang<kangenbo@huawei.com> - 2.0-3.1.8
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:delete sensitive information

* Thu Mar 28 2019 Enbo Kang<kangenbo@huawei.com> - 2.0-3.1.7
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add RELRO and PIE for create-kpatch-module, create-diff-object, create-klp-module

* Sat Mar 23 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.6
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:upgrade to upstream version  0.6.1

* Thu Mar 7 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:add find_special_section_data_arm64 for arm64

* Tue Feb 26 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.4
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add packages required by kpatch and kpatch-runtime

* Mon Feb 25 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.3
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:adapt for native compile_env

* Mon Feb 11 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.2
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:support kernel-4.19

* Thu Dec 20 2018 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.1
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:support c++ kernel module

* Wed Dec 19 2018 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.0
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:support compile kpatch on aarch64

* Fri Nov 23 2018 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-2.7.2
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:fix some kpatch-build fail cases

* Sat Nov 3 2018 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-2.7.1
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:rebase kpatch

* Thu Nov 16 2017 openEuler Builteam <buildteam@openeuler.org> 0.4.0-3
- Package init
