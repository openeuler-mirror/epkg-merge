Name:		tzdata
Version:	2022a
Release:	6
Summary:	Timezone data
License:	Public Domain
URL:		https://www.iana.org/time-zones
Source0:	https://data.iana.org/time-zones/releases/tzdata%{version}.tar.gz
Source1:	https://data.iana.org/time-zones/releases/tzcode%{version}.tar.gz
Source2:	javazic.tar.gz
Source3:	javazic-1.8-37392f2f5d59.tar.xz

Patch6000:	backport-Iran-will-stop-DST-in-2023.patch
Patch6001:	backport-Chile-s-DST-is-delayed-by-a-week-in-September-2022.patch
Patch6002:	backport-Palestine-transitions-are-now-Saturdays-at-02-00.patch
Patch6003:	backport-Tweak-expression-of-Palestine-transition.patch

Patch9000:	bugfix-0001-add-Beijing-timezone.patch
Patch9001:	remove-country-selection-from-tzselect-steps.patch
Patch9002:	remove-ROC-timezone.patch
Patch9003:	rename-Macau-to-Macao.patch
Patch9004:	remove-El_Aaiun-timezone.patch
Patch9005:	remove-Israel-timezone.patch
Patch9006:	skip-check_web-testcase.patch

BuildRequires:	gawk glibc perl-interpreter
BuildRequires:	java-devel
BuildRequires:	glibc-common >= 2.5.90-7
BuildArchitectures: noarch

%description
This package contains data files with rules for various timezones around
the world.

%package        java
Summary:	Timezone data for Java

%description java
This package contains timezone information for use by Java runtimes.

%prep
%autosetup -c -a 1 -p1

mkdir javazic
tar zxf %{SOURCE2} -C javazic
cd javazic

mv sun rht
find . -type f -name '*.java' -print0 \
    | xargs -0 -- sed -i -e 's:sun\.tools\.:rht.tools.:g' \
                         -e 's:sun\.util\.:rht.util.:g'
cd ..

tar xf %{SOURCE3}

echo "%{name}%{version}" >> VERSION

%build
make VERSION=%{version} tzdata%{version}-rearguard.tar.gz
tar zxf tzdata%{version}-rearguard.tar.gz
rm tzdata.zi main.zi

make VERSION=%{version} DATAFORM=rearguard tzdata.zi
make VERSION=%{version} DATAFORM=rearguard main.zi

FILES="africa antarctica asia australasia europe northamerica southamerica
       etcetera backward factory"

mkdir zoneinfo/{,posix,right}
zic -y ./yearistype -d zoneinfo -L /dev/null -p America/New_York $FILES
zic -y ./yearistype -d zoneinfo/posix -L /dev/null $FILES
zic -y ./yearistype -d zoneinfo/right -L leapseconds $FILES

cd javazic
javac -source 1.6 -target 1.6 -classpath . `find . -name \*.java`
cd ..

java -classpath javazic/ rht.tools.javazic.Main -V %{version} \
  -d javazi \
  $FILES javazic/tzdata_jdk/gmt javazic/tzdata_jdk/jdk11_backward

cd javazic-1.8
javac -source 1.8 -target 1.8 -classpath . `find . -name \*.java`
cd ..

java -classpath javazic-1.8 build.tools.tzdb.TzdbZoneRulesCompiler \
    -srcdir . -dstfile tzdb.dat \
    -verbose \
    $FILES javazic-1.8/tzdata_jdk/gmt javazic-1.8/tzdata_jdk/jdk11_backward

%check
make check

%install

rm -fr $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}
cp -prd zoneinfo $RPM_BUILD_ROOT%{_datadir}
install -p -m 644 zone.tab zone1970.tab iso3166.tab leapseconds tzdata.zi $RPM_BUILD_ROOT%{_datadir}/zoneinfo
cp -prd javazi $RPM_BUILD_ROOT%{_datadir}/javazi
mkdir -p $RPM_BUILD_ROOT%{_datadir}/javazi-1.8
install -p -m 644 tzdb.dat $RPM_BUILD_ROOT%{_datadir}/javazi-1.8/

%files
%{_datadir}/zoneinfo
%doc README
%doc theory.html
%doc tz-link.html
%doc tz-art.html
%license LICENSE

%files java
%{_datadir}/javazi
%{_datadir}/javazi-1.8

%changelog
* Mon Oct 10 2022 huangduirong<huangduirong@huawei.com> - 2022a-6
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:move the tzdata rearguard.tar.gz to build

* Fri Sep 2 2022 qinyu<qinyu32@huawei.com> - 2022a-5
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC: Palestine DST transitions time change

* Fri Aug 19 2022 qinyu<qinyu32@huawei.com> - 2022a-4
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:Chile's DST is delayed by a week in September 2022

* Fri Jul 8 2022 liuchao<liuchao173@huawei.com> - 2022a-3
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:remake rearguard version of main.zi to fix check_zishrink_posix fail 

* Thu May 12 2022 liuchao<liuchao173@huawei.com> - 2022a-2
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:Iran will stop DST in 2023

* Mon Apr 18 2022 liuchao<liuchao173@huawei.com> - 2022a-1
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:update to 2022a

* Fri Oct 29 2021 liuchao<liuchao173@huawei.com> - 2021e-1
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:update to 2021e

* Sun Sep 26 2021 liuchao<liuchao173@huawei.com> - 2021b-1
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:update to 2021b

* Thu Sep 23 2021 liuchao<liuchao173@huawei.com> - 2021a-4
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:Samoa no longer observes DST

* Tue Aug 17 2021 liuchao<liuchao173@huawei.com> - 2021a-3
- add factory timezone and enbale make check

* Mon Mar 8 2021 liuchao<liuchao173@huawei.com> - 2021a-2
- Remove useless patches

* Tue Jan 26 2021 liuchao<liuchao173@huawei.com> - 2021a-1
- Upgrade to 2021a

* Fri Jan 22 2021 liuchao<liuchao173@huawei.com> - 2020f-2
- South Sudan changes from +03 to +02 on 2021-02-01

* Tue Jan 12 2021 liuchao<liuchao173@huawei.com> - 2020f-1
- Upgrade to 2020f

* Mon Dec 7 2020 liuchao<liuchao173@huawei.com> - 2020d-5
- backport community patches

* Mon Nov 30 2020 liuchao<liuchao173@huawei.com> - 2020d-4
- backport community patches

* Tue Oct 27 2020 shenkai<shenkai8@huawei.com> - 2020d-3
- backport community patches

* Tue Oct 27 2020 shenkai<shenkai8@huawei.com> - 2020d-2
- backport community patches

* Thu Oct 22 2020 liuchao<liuchao173@huawei.com> - 2020d-1
- Upgrade to 2020d

* Wed Oct 21 2020 liuchao<liuchao173@huawei.com> - 2020c-1
- Upgrade to 2020c and backport community patches

* Wed Oct 14 2020 liuchao<liuchao173@huawei.com> - 2020b-2
- backport community patches

* Sat Oct 10 2020 liuchao<liuchao173@huawei.com> - 2020b-1
- Upgrade to 2020b

* Wed Jun 17 2020 Shinwell Hu <huxinwei@huawei.com> - 2020a-1
- Upgrade to 2020a

* Thu Apr 16 2020 liuchao<liuchao173@huawei.com> - 2019c-1
- Type:recommended
- ID:NA
- SUG:NA
- DESC:rebase to tzdata-2019c

* Mon Mar 23 2020 liuchao<liuchao173@huawei.com> - 2019b-10
- Type:recommended
- ID:NA
- SUG:NA
- DESC:add Beijing timezone in zone1970.tab

* Thu Jan 9 2020 liuchao<liuchao173@huawei.com> - 2019b-9
- Type:recommended
- ID:NA
- SUG:NA
- DESC:remove useless patches

* Wed Jan 8 2020 liuchao<liuchao173@huawei.com> - 2019b-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove Israel and El_Aaiun timezone

* Thu Jan 2 2020 liuchao<liuchao173@huawei.com> - 2019b-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:sync community patches

* Wed Dec 4 2019 liuchao<liuchao173@huawei.com> - 2019b-6
- Type:recommended
- ID:NA
- SUG:NA
- DESC:remove ROC timezone and rename Macau to Macao

* Mon Sep 23 2019 liuchao<liuchao173@huawei.com> -2019b-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: use rearguard data set to fix Casablance DST display error since 2019

* Wed Sep 4 2019 hejingxian<hejingxian@huawei.com> - 2019b-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC: remove  country select operation from tzselect steps.

* Fri Aug 23 2019 wuxu<wuxu.wu@huawei.com> - 2019b-3
- Type:recommended
- ID:NA
- SUG:NA

* Thu Jul 25 2019 luochunsheng<luochunsheng@huawei.com> - 2019b-2
- Type:recommended
- ID:NA
- SUG:NA

* Tue Jul 09 2019 openEuler Buildteam <buildteam@openeuler.org> - 2019b-1
- Rebase to tzdata-2019b
  - Brazil will no longer observe DST going forward.
  - The 2019 spring transition for Palestine occurred 03-29, not 03-30.

* Sun May 5 2019 luochunsheng<luochunsheng@huawei.com> - 2019a-4
- Type:fix
- ID:NA
- SUG:NA
- DESC: Bring back 2019-2037 Morocco Ramadan predictions
	https://www.timeanddate.com/news/time/morocco-changes-clocks-2019.html

* Mon Apr 22 2019 luochunsheng<luochunsheng@huawei.com> - 2019a-3
- Type:NA
- ID:NA
- SUG:NA
- DESC: Revert "Bring back 2019-2037 Morocco Ramadan predictions" to
	 fix Morocco zoneinfo.

* Wed Apr 17 2019 luochunsheng<luochunsheng@huawei.com> - 2019a-2
- Type:NA
- ID:NA
- SUG:NA
- DESC:Quality enhance

* Fri Mar 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 2019a-1
- Rebase to tzdata-2019a
  - Palestine will start DST on 2019-03-30, rather than 2019-03-23 as
    previously predicted.
  - Metlakatla rejoined Alaska time on 2019-01-20, ending its observances
    of Pacific standard time.

* Fri Mar 8 2019 wangjia<wangjia55@huawei.com> - 2018i-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add Beijing timezone

* Tue Jan 15 2019 openEuler Buildteam <buildteam@openeuler.org> - 2018i-1
- Package init
