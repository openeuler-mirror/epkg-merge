#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {

sslarch=%{_os}-%{_target_cpu}
%ifarch x86_64 aarch64
sslflags=enable-ec_nistp_64_gcc_128
%endif

RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY $RPM_LD_FLAGS"
./Configure \
    --prefix=%{_prefix} \
    --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
    zlib enable-camellia enable-seed enable-rfc3779 enable-sctp \
    enable-cms enable-md2 enable-rc5 enable-ssl3 enable-ssl3-method \
    enable-weak-ssl-ciphers \
    no-mdc2 no-ec2m enable-sm2 enable-sm3 enable-sm4 enable-tlcp \
    shared ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\""'

%make_build all

%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{version}.hmac \
    ln -sf .libcrypto.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{soversion}.hmac \
    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{version}.hmac \
    ln -sf .libssl.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{soversion}.hmac \
%{nil}

}

install() {

%make_install

rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`
ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_pkgdocdir}/Makefile.certificate

mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc/*.pl $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/misc/tsget $RPM_BUILD_ROOT%{_bindir}


mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/{certs,crl,newcerts,private}
chmod 700 $RPM_BUILD_ROOT%{_sysconfdir}/pki/CA/private

touch -r %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/{openssl.cnf,ct_log_list.cnf}


%define manpostfix _openssl
pushd $RPM_BUILD_ROOT%{_mandir}
ln -s -f config.5 man5/openssl.cnf.5
for manpage in man*/* ; do
if [ -L ${manpage} ]; then
targetfile=`ls -l ${manpage} | awk '{print $NF}'`
ln -sf ${targetfile}%{manpostfix} ${manpage}%{manpostfix}
rm -f ${manpage}
else
mv ${manpage} ${manpage}%{manpostfix}
fi
done
popd

sed -i '/^\#ifndef OPENSSL_NO_SSL_TRACE/i\

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/*.dist

}

check() {
LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
crypto/fips/fips_standalone_hmac libcrypto.so.%{soversion} >.libcrypto.so.%{soversion}.hmac
ln -s .libcrypto.so.%{soversion}.hmac .libcrypto.so.hmac
crypto/fips/fips_standalone_hmac libssl.so.%{soversion} >.libssl.so.%{soversion}.hmac
ln -s .libssl.so.%{soversion}.hmac .libssl.so.hmac
OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE
make test || :

}

