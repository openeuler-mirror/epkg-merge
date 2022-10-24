* Tue May 24 2022 fengtao <fengtao40@huawei.com> - 0.15-5
- we got upgrade error when upgrade json-c from very low version,
for example json-c-0.11-5. because old version has a softlink:
/usr/include/json-c  --> /usr/include/json
and now, softlink has been removed. so, we fix this in pretrans

* Fri May 6 2022 wuchaochao <cyanrose@yeah.net> - 0.15-4
- add   backport-json-escape-str-avoid-harmless-unsigned-integer-overflow.patch

* Thu Apr 7 2022 wuchaochao <cyanrose@yeah.net> - 0.15-3
- add check

* Fri Mar 25 2022 wuchaochao <cyanrose@yeah.net> - 0.15-2
- move json-c

* Tue Sep 14 2021 hanhui <hanhui15@huawei.com> - 0.15-1
- update to 0.15

* Thu Sep 9 2021 liuyumeng <liuyumeng5@huawei.com> - 0.13.1-9
- fix broken RDRAND causes infinite looping

* Tue Jul 21 2020 wangye <wangye70@huawei.com> - 0.13.1-8
- fix hardlink path

* Fri May 22 2020 ruanweidong <ruanweidong1@huawei.com> -0.13.1-7
- fix CVE-2020-12762

* Sat Mar 21 2020 songnannan <songnannan2@huawei.com> - 0.13.1-6
- delete the check

* Tue Mar 3 2020 songnannan<songnannan2@huawei.com> - 0.13.1-5
- bugfix in oss-fuzz

* Thu Sep 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.13.1-4
- Package init
