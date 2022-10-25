#!/usr/bash

prep() {
%setup -q

%patch0 -p1 -b .PIE
%patch1 -p1 -b .redhat_doc
%patch2 -p1 -b .64bit
%patch3 -p1 -b .rh490837
%patch4 -p1 -b .rh645544
%patch5 -p1 -b .libdb
%patch9 -p1 -b .fips-tests
%patch10 -p1 -b .rh1666814

%patch11 -p1
%patch12 -p1
%patch13 -p1

%if %{with PKCS11}
%patch6 -p1 -b .config-pkcs11
cp -r bin/named{,-pkcs11}
cp -r bin/dnssec{,-pkcs11}
cp -r lib/dns{,-pkcs11}
cp -r lib/ns{,-pkcs11}
%patch7 -p1 -b .dist_pkcs11
%patch8 -p1 -b .kyua-pkcs11
%endif

%ifarch sparcv9 sparc64 s390 s390x
for i in bin/named/{,unix}/Makefile.in; do
sed -i 's|fpie|fPIE|g' $i
done
%endif

sed -e 's|"$TOP/config.guess"|"$TOP_SRCDIR/config.guess"|' -i bin/tests/system/ifconfig.sh
:;


}

build() {
%define _configure "../configure"

%define unit_prepare_build() \
  cp -uv Kyuafile "%{1}/" \
  find lib -name 'K*.key' -exec cp -uv '{}' "%{1}/{}" ';' \
  find lib -name 'Kyuafile' -exec cp -uv '{}' "%{1}/{}" ';' \
  find lib -name 'testdata' -type d -exec cp -Tav '{}' "%{1}/{}" ';' \
  find lib -name 'testkeys' -type d -exec cp -Tav '{}' "%{1}/{}" ';' \

%define systemtest_prepare_build() \
  cp -Tuav bin/tests "%{1}/bin/tests/" \
  cp -uv version "%{1}" \

CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
%if %{with TSAN}
CFLAGS+=" -O1 -fsanitize=thread -fPIE -pie"
%endif
export CFLAGS
export STD_CDEFINES="$CPPFLAGS"



libtoolize -c -f; aclocal -I libtool.m4 --force; autoconf -f

mkdir build

%if %{with DLZ}
# DLZ modules do not support oot builds. Copy files into build
mkdir -p build/contrib/dlz
cp -frp contrib/dlz/modules build/contrib/dlz/modules
%endif

pushd build
LIBDIR_SUFFIX=
export LIBDIR_SUFFIX
%configure %%{env.configureFlags} --localstatedir=%{_var} --includedir=%{_includedir}/bind9 \
%if %{with GEOIP2}
--with-maxminddb \
%endif
%if %{with PKCS11}
--enable-native-pkcs11 \
  --with-pkcs11=%{_libdir}/pkcs11/libsofthsm2.so \
%endif
%if %{with GSSTSIG}
--with-gssapi=yes \
%endif
%if %{with LMDB}
--with-lmdb=yes \
%else
--with-lmdb=no \
%endif
%if %{with JSON}
--without-libjson --with-json-c \
%endif
%if %{with DNSTAP}
--enable-dnstap \
%endif
%if %{with UNITTEST}
--with-cmocka \
%endif
;
%if %{with DNSTAP}
pushd lib
SRCLIB="../../../lib"
(cd dns && ln -s ${SRCLIB}/dns/dnstap.proto)
%if %{with PKCS11}
(cd dns-pkcs11 && ln -s ${SRCLIB}/dns-pkcs11/dnstap.proto)
%endif
popd
%endif

%if %{with DOCPDF}
# avoid using home for pdf latex files
export TEXMFVAR="`pwd`"
export TEXMFCONFIG="`pwd`"
fmtutil-user --listcfg || :
fmtutil-user --missing || :
%endif

%make_build

pushd bin/dig
make man
popd
pushd bin/python
make man
popd

%if %{with DOC}
make doc
%endif

%if %{with DLZ}
pushd contrib/dlz/modules
for DIR in mysql mysqldyn; do
sed -e 's/@DLZ_DRIVER_MYSQL_INCLUDES@/$(shell mysql_config --cflags)/' \
        -e 's/@DLZ_DRIVER_MYSQL_LIBS@/$(shell mysql_config --libs)/' \
        $DIR/Makefile.in > $DIR/Makefile
done
for DIR in filesystem ldap mysql mysqldyn sqlite3; do
make -C $DIR CFLAGS="-fPIC -I../include $CFLAGS $LDFLAGS"
done
popd
%endif
popd # build

%unit_prepare_build build
%systemtest_prepare_build build

}

check() {
%if %{with PKCS11} && (%{with UNITTEST} || %{with SYSTEMTEST})
# Tests require initialization of pkcs11 token
eval "$(bash %{SOURCE23} -A "`pwd`/softhsm-tokens")"
%endif

%if %{with TSAN}
export TSAN_OPTIONS="log_exe_name=true log_path=ThreadSanitizer exitcode=0"
%endif

%if %{with UNITTEST}
pushd build
CPUS=$(lscpu -p=cpu,core | grep -v '^#' | wc -l)
if [ "$CPUS" -gt 16 ]; then
ORIGFILES=$(ulimit -n)
ulimit -n 4096 || : # Requires on some machines with many cores
fi
export ISC_TASK_WORKERS=8
make unit
e=$?
if [ "$e" -ne 0 ]; then
echo "ERROR: this build of BIND failed 'make unit'. Aborting."
exit $e;
fi;

[ "$CPUS" -gt 16 ] && ulimit -n $ORIGFILES || :
popd
## End of UNITTEST
%endif

%if %{with SYSTEMTEST}
# Runs system test if ip addresses are already configured
# or it is able to configure them
if perl bin/tests/system/testsock.pl
then
CONFIGURED=already
else
CONFIGURED=
sh bin/tests/system/ifconfig.sh up
perl bin/tests/system/testsock.pl && CONFIGURED=build
fi
if [ -n "$CONFIGURED" ]
then
set -e
pushd build/bin/tests
chown -R ${USER} . # Can be unknown user
%make_build test 2>&1 | tee test.log
e=$?
popd
[ "$CONFIGURED" = build ] && sh bin/tests/system/ifconfig.sh down
if [ "$e" -ne 0 ]; then
echo "ERROR: this build of BIND failed 'make test'. Aborting."
exit $e;
fi;
else
echo 'SKIPPED: tests require root, CAP_NET_ADMIN or already configured test addresses.'
fi
%endif
:

}

install() {
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/{bind,named}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/named/{slaves,data,dynamic}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/{man1,man5,man8}
mkdir -p ${RPM_BUILD_ROOT}/run/named
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/log

for D in %{chroot_create_directories}
do
mkdir -p ${RPM_BUILD_ROOT}/%{chroot_prefix}${D}
done

pushd ${RPM_BUILD_ROOT}/%{chroot_prefix}/var
ln -s ../run run
popd

touch ${RPM_BUILD_ROOT}/%{chroot_prefix}%{_sysconfdir}/named.conf

pushd build
%make_install
popd
rpm -E %{_unitdir}

rm -f ${RPM_BUILD_ROOT}/etc/bind.keys

mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE15} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE16} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE20} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE21} ${RPM_BUILD_ROOT}%{_unitdir}

%if %{with PKCS11}
install -m 644 %{SOURCE22} ${RPM_BUILD_ROOT}%{_unitdir}
%else
# Not packaged without PKCS11
find ${RPM_BUILD_ROOT}%{_includedir}/bind9/pk11 ${RPM_BUILD_ROOT}%{_includedir}/bind9/pkcs11 \
  -name '*.h' \! -name site.h -delete

%endif

mkdir -p ${RPM_BUILD_ROOT}%{_libexecdir}
install -m 755 %{SOURCE17} ${RPM_BUILD_ROOT}%{_libexecdir}/setup-named-chroot.sh
install -m 755 %{SOURCE18} ${RPM_BUILD_ROOT}%{_libexecdir}/generate-rndc-key.sh

%if %{with PKCS11}
install -m 755 %{SOURCE23} ${RPM_BUILD_ROOT}%{_libexecdir}/setup-named-softhsm.sh
%endif

install -m 644 %SOURCE3 ${RPM_BUILD_ROOT}/etc/logrotate.d/named
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/named
install -m 644 %{SOURCE24} ${RPM_BUILD_ROOT}%{_sysconfdir}/named-chroot.files

%if %{with DLZ}
pushd build
pushd contrib/dlz/modules
for DIR in filesystem ldap mysql mysqldyn sqlite3; do
%make_install -C $DIR libdir=%{_libdir}/named
done
pushd ${RPM_BUILD_ROOT}/%{_libdir}/bind
cp -s ../named/dlz_*.so .
popd
mkdir -p doc/{mysql,mysqldyn}
cp -p mysqldyn/testing/README doc/mysqldyn/README.testing
cp -p mysqldyn/testing/* doc/mysqldyn
cp -p mysql/testing/* doc/mysql
popd
popd
%endif

install -m 644 lib/isc/unix/errno2result.h ${RPM_BUILD_ROOT}%{_includedir}/bind9/isc

find ${RPM_BUILD_ROOT}/%{_libdir} -name '*.la' -exec '/bin/rm' '-f' '{}' ';';

%if %{with PKCS11}
pushd ${RPM_BUILD_ROOT}%{_mandir}/man8
ln -s named.8.gz named-pkcs11.8.gz
ln -s dnssec-checkds.8.gz dnssec-checkds-pkcs11.8.gz
ln -s dnssec-dsfromkey.8.gz dnssec-dsfromkey-pkcs11.8.gz
ln -s dnssec-importkey.8.gz dnssec-importkey-pkcs11.8.gz
ln -s dnssec-keyfromlabel.8.gz dnssec-keyfromlabel-pkcs11.8.gz
ln -s dnssec-keygen.8.gz dnssec-keygen-pkcs11.8.gz
ln -s dnssec-revoke.8.gz dnssec-revoke-pkcs11.8.gz
ln -s dnssec-settime.8.gz dnssec-settime-pkcs11.8.gz
ln -s dnssec-signzone.8.gz dnssec-signzone-pkcs11.8.gz
ln -s dnssec-verify.8.gz dnssec-verify-pkcs11.8.gz
popd
%endif

%if %{without DNSTAP}
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/dnstap-read.1* || true
%endif
%if %{without LMDB}
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man8/named-nzd2nzf.8* || true
%endif

pushd ${RPM_BUILD_ROOT}%{_mandir}/man8
ln -s ddns-confgen.8.gz tsig-keygen.8.gz
ln -s named-checkzone.8.gz named-compilezone.8.gz
popd

%if %{with DOC}
mkdir -p ${RPM_BUILD_ROOT}%{_pkgdocdir}
cp -a build/doc/arm/_build/html ${RPM_BUILD_ROOT}%{_pkgdocdir}
rm -rf ${RPM_BUILD_ROOT}%{_pkgdocdir}/html/.{buildinfo,doctrees}
# Backward compatible link to 9.11 documentation
(cd ${RPM_BUILD_ROOT}%{_pkgdocdir} && ln -s html/index.html Bv9ARM.html)
# Share static data from original sphinx package
for DIR in %{python3_sitelib}/sphinx_rtd_theme/static/*
do
BASE=$(basename -- "$DIR")
BINDTHEMEDIR="${RPM_BUILD_ROOT}%{_pkgdocdir}/html/_static/$BASE"
if [ -d "$BINDTHEMEDIR" ]; then
rm -rf "$BINDTHEMEDIR"
ln -s "$DIR" "$BINDTHEMEDIR"
fi
done
%endif
%if %{with DOCPDF}
cp -a build/doc/arm/Bv9ARM.pdf ${RPM_BUILD_ROOT}%{_pkgdocdir}
%endif

touch ${RPM_BUILD_ROOT}%{_localstatedir}/log/named.log

install -m 640 %{SOURCE5} ${RPM_BUILD_ROOT}%{_sysconfdir}/named.conf
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/rndc.{key,conf}
install -m 644 %{SOURCE12} ${RPM_BUILD_ROOT}%{_sysconfdir}/named.root.key
install -m 644 %{SOURCE14} ${RPM_BUILD_ROOT}%{_sysconfdir}/trusted-key.key
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/named

mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/named
install -m 640 %{SOURCE6} ${RPM_BUILD_ROOT}%{_localstatedir}/named/named.ca
install -m 640 %{SOURCE7} ${RPM_BUILD_ROOT}%{_localstatedir}/named/named.localhost
install -m 640 %{SOURCE8} ${RPM_BUILD_ROOT}%{_localstatedir}/named/named.loopback
install -m 640 %{SOURCE9} ${RPM_BUILD_ROOT}%{_localstatedir}/named/named.empty
install -m 640 %{SOURCE10} ${RPM_BUILD_ROOT}%{_sysconfdir}/named.rfc1912.zones

mkdir -p sample/etc sample/var/named/{data,slaves}
install -m 644 %{SOURCE11} sample/etc/named.conf
install -m 644 %{SOURCE5} named.conf.default
install -m 644 %{SOURCE10} sample/etc/named.rfc1912.zones
install -m 644 %{SOURCE7} %{SOURCE8} %{SOURCE9}  sample/var/named
install -m 644 %{SOURCE6} sample/var/named/named.ca
for f in my.internal.zone.db slaves/my.slave.internal.zone.db slaves/my.ddns.internal.zone.db my.external.zone.db; do
echo '@ in soa localhost. root 1 3H 15M 1W 1D
ns localhost.' > sample/var/named/$f;
done
:;

mkdir -p ${RPM_BUILD_ROOT}%{_tmpfilesdir}
install -m 644 %{SOURCE13} ${RPM_BUILD_ROOT}%{_tmpfilesdir}/named.conf

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/rwtab.d
install -m 644 %{SOURCE19} ${RPM_BUILD_ROOT}%{_sysconfdir}/rwtab.d/named

}

