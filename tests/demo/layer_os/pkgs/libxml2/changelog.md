* Tue Sep 13 2022 fuanan <fuanan3@h-partners.com> - 2.9.14-2
- Fix Obsoletes in spec

* Wed Jul 13 2022 fuanan <fuanan3@h-partners.com> - 2.9.14-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Upgrade to upstream v2.9.14 and Cleanup duplicate installation

* Fri Jun 24 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix memory leaks in xmlACatalogAdd when xmlHashAddEntry failed

* Thu Jun 16 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix memory leaks for xmlACatalogAdd

* Mon May 09 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-6
- Type:CVE
- ID:CVE-2022-29824
- SUG:NA
- DESC:fix CVE-2022-29824

* Wed Mar 09 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-5
- Type:CVE
- ID:CVE-2022-23308
- SUG:NA
- DESC:fix CVE-2022-23308

* Fri Feb 11 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:use upstream patch refix heap-use-after-free in xmlAddNextSibling and xmlAddChild

* Fri Nov 12 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.12-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add backport bug fixes.
work around lxml API abuse
fix regression in xmlNodeDumpOutputInternal
fix whitespace when serializing empty HTML documents
forbid epsilon-reduction of final states
fix buffering in xmlOutputBufferWrite

* Thu Nov 11 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.12-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix heap-use-after-free in xmlAddNextSibling and xmlAddChild

* Wed Nov 10 2021 Zhipeng Xie <xiezhipeng1@huawei.com> - 2.9.12-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:upgrade to upstream v2.9.12

* Tue Nov 9 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.10-19
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix memleaks in xmlXIncludeProcessFlags

* Sat Oct 30 2021 huangduirong <huangduirong@huawei.com> - 2.9.10-18
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix fuzz issues, fix null-deref in xmlSchemaGetComponentTargetNs

* Sat Oct 23 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.10-17
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix fuzz issues
fix memory leaks in XPointer string-range function
fix null pointer deref in xmlXPtrRangeInsideFunction
stop using maxParserDepth in xpath.c
hardcode maximum XPath recursion depth
fix XPath recursion limit

* Thu Oct 21 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.10-16
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix fuzz issues
fix heap-use-after-free in xmlXIncludeIncludeNode
fix stack overflow in xmlDocDumpMemory
fix stack overflow in htmlDocContentDumpOutput

* Wed Jun 2 2021 guoxiaoqi <guoxiaoqi2@huawei.com> - 2.9.10-15
- Type:CVE
- ID:CVE-2021-3541
- SUG:NA
- DESC:fix CVE-2021-3541

* Sat May 29 2021 zoulin <zoulin13@huawei.com> - 2.9.10-14
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:[add] patches from upstream
Fix-handling-of-unexpected-EOF-in-xmlParseContent.patch
Fix-line-numbers-in-error-messages-for-mismatched-ta.patch
Fix-null-deref-in-legacy-SAX1-parser.patch
update-for-xsd-language-type-check.patch
Fix-dangling-pointer-with-xmllint-dropdtd.patch
Fix-duplicate-xmlStrEqual-calls-in-htmlParseEndTag.patch
Fix-exponential-behavior-with-recursive-entities.patch
Fix-quadratic-behavior-when-looking-up-xml-attribute.patch
Fix-use-after-free-with-xmllint-html-push.patch
Fix-xmlGetNodePath-with-invalid-node-types.patch
Stop-checking-attributes-for-UTF-8-validity.patch

* Fri May 28 2021 guoxiaoqi <guoxiaoqi2@huawei.com> - 2.9.10-13
- Type:CVE
- ID:CVE-2021-3517, CVE-2021-3518
- SUG:NA
- DESC:fix CVE-2021-3517 and CVE-2021-3518

* Wed May 26 2021 yangkang <yangkang90@huawei.com> - 2.9.10-12
- Type:CVE
- ID:CVE-2021-3537
- SUG:NA
- DESC:fix CVE-2021-3537

* Tue Mar 2 2021 Lirui <lirui130@huawei.com> - 2.9.10-11
- fix problems detected by oss-fuzz test

* Thu Nov 12 2020 Liquor <lirui130@huawei.com> - 2.9.10-10
- fix problems detected by oss-fuzz test

* Thu Oct 29 2020 panxiaohe <panxiaohe@huawei.com> - 2.9.10-9
- remove subpackage python2-libxml2

* Mon Sep 14 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.9.10-8
- revert Don-t-try-to-handle-namespaces-when-building-HTML-do.patch.
rubygem-nokogoro test case fail,because this patch remove xml namespace function.

* Thu Sep 10 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.9.10-7
- Fixed some issues found in fuzzing testcases

* Fri Aug 28 2020 zoulin <zoulin13@huawei.com> - 2.9.10-6
- Fix more quadratic runtime issues in HTML push parse
- Fix reset HTML parser input before reporting error

* Wed Aug 12 2020 Liquor <lirui130@huawei.com> - 2.9.10-5
- Limit regexp nesting depth
- Fix exponential runtime in xmlFARecurseDeterminism

* Mon Aug 3 2020 Liquor <lirui130@huawei.com> - 2.9.10-4
- Fix integer overflow in xmlFAParseQuantExact

* Tue Jul 28 2020 shenyangyang <shenyangyang4@huawei.com> - 2.9.10-3
- Fix-use-after-free-with-validating-reader and
Never-expand-parameter-entities-in-text-declaration

* Fri Jul 3 2020 wangchen <wangchen137@huawei.com> - 2.9.10-2
- Sync some patches from community

* Fri Apr 24 2020 BruceGW <gyl93216@163.com> - 2.9.10-1
- update upstream to 2.9.10

* Tue Mar 17 2020 Leo Fang<leofang_94@163.com> - 2.9.8-9
- Sync some patches from community

* Thu Dec 19 2019 openEuler Buildteam <buildteam@openEuler.org> - 2.9.8-8
- Delete unused infomation

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.8-7
- Fix memory leak in xmlSchemaValidateStream

* Fri Sep 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.8-6
- Delete redundant information

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.8-5
- Delete epoch

* Thu Sep 5 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.8-2
- Backport upstream patches and merge static library to devel package

