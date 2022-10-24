#!/usr/bash

prep() {
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

}

build() {
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

}

check() {
make check

}

install() {

rm -fr $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}
cp -prd zoneinfo $RPM_BUILD_ROOT%{_datadir}
install -p -m 644 zone.tab zone1970.tab iso3166.tab leapseconds tzdata.zi $RPM_BUILD_ROOT%{_datadir}/zoneinfo
cp -prd javazi $RPM_BUILD_ROOT%{_datadir}/javazi
mkdir -p $RPM_BUILD_ROOT%{_datadir}/javazi-1.8
install -p -m 644 tzdb.dat $RPM_BUILD_ROOT%{_datadir}/javazi-1.8/

}

