%define soversion 1.1
Name:        openssl
Epoch:       1
Version:     1.1.1m
Release:     7
Summary:     Cryptography and SSL/TLS Toolkit
License:     OpenSSL and SSLeay
URL:         https://www.openssl.org/
Source0:     https://www.openssl.org/source/%{name}-%{version}.tar.gz
Source1:     Makefile.certificate
Patch1:      openssl-1.1.1-build.patch
Patch2:      openssl-1.1.1-fips.patch
Patch3:      CVE-2022-0778-Add-a-negative-testcase-for-BN_mod_sqrt.patch
Patch4:      CVE-2022-0778-Fix-possible-infinite-loop-in-BN_mod_sqrt.patch
Patch5:      CVE-2022-1292.patch
Patch6:      Backport-Support-raw-input-data-in-apps-pkeyutl.patch
Patch7:      Backport-Fix-no-ec-no-sm2-and-no-sm3.patch
Patch8:      Backport-Support-SM2-certificate-verification.patch
Patch9:      Backport-Guard-some-SM2-functions-with-OPENSSL_NO_SM2.patch
Patch10:     Backport-Add-test-cases-for-SM2-cert-verification.patch
Patch11:     Backport-Add-documents-for-SM2-cert-verification.patch
Patch12:     Backport-Fix-a-memleak-in-apps-verify.patch
Patch13:     Backport-Skip-the-correct-number-of-tests-if-SM2-is-disabled.patch
Patch14:     Backport-Make-X509_set_sm2_id-consistent-with-other-setters.patch
Patch15:     Backport-Support-SM2-certificate-signing.patch
Patch16:     Backport-Support-parsing-of-SM2-ID-in-hexdecimal.patch
Patch17:     Backport-Fix-a-double-free-issue-when-signing-SM2-cert.patch
Patch18:     Backport-Fix-a-document-description-in-apps-req.patch
Patch19:     Backport-Update-expired-SCT-certificates.patch
Patch20:     Backport-ct_test.c-Update-the-epoch-time.patch
Patch21:     Feature-Support-TLCP-protocol.patch
Patch22:     Feature-X509-command-supports-SM2-certificate-signing-with-default-sm2id.patch
Patch23:     CVE-2022-2068-Fix-file-operations-in-c_rehash.patch
Patch24:     CVE-2022-2097-Fix-AES-OCB-encrypt-decrypt-for-x86-AES-NI.patch

BuildRequires: gcc perl make lksctp-tools-devel coreutils util-linux zlib-devel
Requires:    coreutils %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:   openssl-SMx < %{epoch}:%{version}-%{release}
Provides:    openssl-SMx = %{epoch}:%{version}-%{release}

%description
OpenSSL is a robust, commercial-grade, and full-featured toolkit for the
Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols.

%package libs
Summary:      A general purpose cryptography library with TLS implementation
Group:        System Environment/Libraries
Requires:     ca-certificates >= 2008-5
Requires:     crypto-policies >= 20180730
Recommends:   openssl-pkcs11%{?_isa}
Obsoletes:    openssl < 1:1.0.1-0.3.beta3
Obsoletes:    openssl-fips < 1:1.0.1e-28
Provides:     openssl-fips = %{epoch}:%{version}-%{release}
Obsoletes:    openssl-SMx-libs < %{epoch}:%{version}-%{release}
Provides:     openssl-SMx-libs = %{epoch}:%{version}-%{release}

%description libs
The openssl-libs package contains the libraries that are used
by various applications which support cryptographic algorithms
and protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Requires: perl-interpreter
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%package devel
Summary:   Development files for openssl
Requires:  %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: krb5-devel zlib-devel pkgconfig
Obsoletes: openssl-static < %{epoch}:%{version}-%{release}
Provides:  openssl-static = %{epoch}:%{version}-%{release} openssl-static%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: openssl-SMx-devel < %{epoch}:%{version}-%{release}
Provides:  openssl-SMx-devel = %{epoch}:%{version}-%{release}

%description devel
%{summary}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build

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

%install

%make_install

# rename so name with actual version
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
# create symbolic link
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


# rename man pages avoid conflicting with other man pages in system
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

# Next step of gradual disablement of ssl3.
# Make SSL3 disappear to newly built dependencies.
sed -i '/^\#ifndef OPENSSL_NO_SSL_TRACE/i\
#ifndef OPENSSL_NO_SSL3\
# define OPENSSL_NO_SSL3\
#endif' $RPM_BUILD_ROOT/%{_prefix}/include/openssl/opensslconf.h

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/*.dist

%check
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

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%doc AUTHORS CHANGES FAQ NEWS README
%{_pkgdocdir}/Makefile.certificate
%{_bindir}/openssl

%files libs
%defattr(-,root,root)
%license LICENSE
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%config(noreplace) %{_sysconfdir}/pki/tls/ct_log_list.cnf
%{_libdir}/libcrypto.so.%{version}
%{_libdir}/libcrypto.so.%{soversion}
%{_libdir}/libssl.so.%{version}
%{_libdir}/libssl.so.%{soversion}
%{_libdir}/engines-%{soversion}
%attr(0644,root,root) %{_libdir}/.libcrypto.so.*.hmac
%attr(0644,root,root) %{_libdir}/.libssl.so.*.hmac

%files devel
%defattr(-,root,root)
%doc doc/dir-locals.example.el doc/openssl-c-indent.el
%{_prefix}/include/openssl
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_libdir}/*.a

%files help
%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_pkgdocdir}/html/

%files perl
%{_bindir}/c_rehash
%{_bindir}/*.pl
%{_bindir}/tsget
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts

%ldconfig_scriptlets libs

%changelog
* Tue Sep 13 2022 wangcheng <wangcheng156@huawei.com> - 1:1.1.1m-7
- add provides for openssl-SMx

* Tue Jul 12 2022 wangcheng <wangcheng156@huawei.com> - 1:1.1.1m-6
- fix CVE-2022-2097

* Thu Jun 30 2022 wangcheng <wangcheng156@huawei.com> - 1:1.1.1m-5
- fix CVE-2022-2068

* Wed Jun 29 2022 shichuchao <shichuchao@huawei.com> - 1:1.1.1m-4
- x509 command support SM2 signing with default sm2id

* Thu Jun 9 2022 shichuchao <shichuchao@huawei.com> - 1:1.1.1m-3
- support sm2 certificate sign and verify
- fix ct test errors
- add TLCP feature

* Mon May 16 2022 zhouchenchen <zhouchenchen@huawei.com> - 1:1.1.1m-2
- fix the CVE-2022-1292

* Thu Mar 24 2022 duyiwei <duyiwei@kylinos.cn> - 1:1.1.1m-1
- update openssl-1.1.1f to openssl-1.1.1m
- add subpackage openssl-perl
- fix the cve-2022-0778

* Wed Dec 8 2021 lujie42 <lujie42@huawei.com> - 1:1.1.1l-1
- update openssl-1.1.1f to openssl-1.1.1l

* Fri Sep 24 2021 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1f-9
- bugfix Overflow when printing Thawte Strong Extranet

* Sat Sep 18 2021 zhuyan <zhuyan34@huawei.com> - 1:1.1.1f-8
- fix software package format problem

* Mon Aug 30 2021 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1f-7
- fix the CVE-2021-3711 and CVE-2021-3712

* Tue Jun 29 2021 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1f-6
- add perl BuildRequires

* Wed Apr 7 2021 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1f-5
- fix CVE-2021-3449

* Wed Mar 10 2021 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1f-4
- fix CVE-2021-23840 and CVE-2021-23841

* Tue Jan 19 2021 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1f-3
- fix CVE-2020-1971

* Fri Sep 11 2020 Liquor <lirui130@huawei.com> - 1:1.1.1f-2
- provides openssl-perl

* Tue May 12 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1f-1
- update openssl-1.1.1d to openssl-1.1.1f and fix CVE-2020-1967

* Wed Mar 18 2020 steven <steven_ygui@163.com> - 1:1.1.1d-9
- fix division zero issue which found by oss-fuzz

* Tue Mar 3 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1d-8
- add missiong /sbin/ldconfig

* Tue Mar 3 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1d-7
- Fix problem caused by missing hmac files

* Mon Feb 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1d-6
- add openssl-libs containing dynamic library for openssl

* Sun Jan 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1d-5
- add obsoletes

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1d-4
- clean code

* Fri Jan 10 2020 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1d-3
- delete unused files

* Fri Dec 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1d-2
- modify obsoletes

* Mon Dec 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1d-1
- update to 1:1.1.1d

* Thu Nov 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1c-5
- enable sm2 and sm4

* Fri Oct 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1c-4
- Add missing openssl/fips.h

* Thu Oct 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1c-3
- Add buildrequires zlib-devel

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1c-2
- Adjust requires

* Mon Sep 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 1:1.1.1c-1
- Package init
