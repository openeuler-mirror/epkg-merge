%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%define rsyslog_docdir %{_docdir}/rsyslog

# If the systemd server exists, the macro value of systemd_lived is 1, otherwise it is 0
%define systemd_lived 1

Name:           rsyslog
Version:        8.2110.0
Release:        11
Summary:        The rocket-fast system for log processing
License:        (GPLv3+ and ASL 2.0)
URL:            http://www.rsyslog.com/
Source0:        http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1:        http://www.rsyslog.com/files/download/rsyslog/%{name}-doc-%{version}.tar.gz
Source2:        rsyslog.conf
Source3:        rsyslog.sysconfig
Source4:        rsyslog.log
Source5:        os_rotate_and_save_log.sh
Source6:        os_check_timezone_for_rsyslog.sh
Source7:        timezone.cron
Source8:        rsyslog.service
Source9:	timezone_update.sh

Patch9000:      rsyslog-8.24.0-ensure-parent-dir-exists-when-writting-log-file.patch
Patch9001:      bugfix-rsyslog-7.4.7-imjournal-add-monotonic-timestamp.patch
Patch9002:      bugfix-rsyslog-7.4.7-add-configuration-to-avoid-memory-leak.patch
Patch9003:      rsyslog-8.37.0-initialize-variables-and-check-return-value.patch
%if %{systemd_lived} == 1
Patch9004:      print-main-queue-info-to-journal-when-queue-full.patch
Patch9005:      print-main-queue-info-to-journal-when-receive-USR1-signal.patch
%endif
Patch9006:      bugfix-CVE-2022-24903.patch

Patch6000:      backport-testbench-skip-omfwd_fast_imuxsock.sh-if-liblogging-stdlog-is-not-available.patch
Patch6001:      backport-Fixes-4395-by-correctly-checking-for-EPIPE.patch
Patch6002:      backport-rsyslogd-adjust-the-order-of-doHUP-and-processImInte.patch
Patch6003:      backport-gnutls-bugfix-Fix-error-handling-in-gtlsRecordRecv.patch
Patch6004:      backport-Fix-non-null-terminated-string-used-with-strlen.patch
Patch6005:      backport-tcpsrv-do-not-decrease-number-of-to-be-processed-fds.patch
Patch6006:      backport-imptcp-bugfix-worker-thread-starvation-on-extreme-tr.patch
Patch6007:      backport-Fix-memory-leak-when-globally-de-initialize-GnuTLS.patch
Patch6008:      backport-Fix-memory-leak-when-free-action-worker-data-table.patch 

BuildRequires:  gcc autoconf automake bison dos2unix flex pkgconfig python3-docutils libtool
BuildRequires:  libgcrypt-devel libuuid-devel zlib-devel krb5-devel libnet-devel gnutls-devel
BuildRequires:  libfastjson-devel >= 0.99.8 libestr-devel >= 0.1.9  
BuildRequires:  mariadb-connector-c-devel net-snmp-devel qpid-proton-c-devel libcurl-devel
%if %{systemd_lived} == 1
BuildRequires:  systemd-devel >= 204-8
%endif
Requires:       logrotate >= 3.5.2 bash >= 2.0 
%{?systemd_requires}

Provides:       syslog
Obsoletes:      sysklogd < 1.5-11

%description
RSYSLOG is the rocket-fast system for log processing.It offers high-performance,
great security features and a modular design. While it started as a regular syslogd,
rsyslog has evolved into a kind of swiss army knife of logging, being able to
accept inputs from a wide variety of sources, transform them, and output to the
results to diverse destinations.

RSYSLOG can deliver over one million messages per second to local destinations when
limited processing is applied. Even with remote destinations and more elaborate
processing the performance is usually considered “stunning”.

%package hiredis
Summary: Redis support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: hiredis-devel

%description hiredis
This package provides support from redis.

%package kafka
Summary: Provides the omkafka module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librdkafka-devel

%description kafka
This package provides support from kafka.

%package mmnormalize
Summary: Log normalization support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libestr-devel liblognorm-devel >= 1.0.2

%description mmnormalize
This module provides the capability to normalize log messages via liblognorm.

%package mmkubernetes
Summary: Provides the mmkubernetes module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libcurl-devel

%description mmkubernetes
This package provides support for kubernetes to add container metadata.

%package mongodb
Summary: MongoDB support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mongo-c-driver-devel snappy-devel cyrus-sasl-devel

%description mongodb
This package provides support from mongodb.

%package omamqp1
Summary: Provides the omamqp1 module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: qpid-proton-c-devel

%description omamqp1
The omamqp1 output module can be used to send log messages via an AMQP
1.0-compatible messaging bus.

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%package rabbitmq
Summary: RabbitMQ support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librabbitmq-devel >= 0.2

%description rabbitmq
This package provides support from rabbitmq.

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librelp-devel >= 1.0.3

%description relp
The rsyslog-relp package contains the rsyslog plugins that provide
the ability to receive syslog messages via the reliable RELP
protocol.

%package snmp
Summary: SNMP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: net-snmp-devel 

%description snmp
The rsyslog-snmp package contains the rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%package crypto
Summary: Encryption support
Requires: %name = %version-%release

%description crypto
This package contains a module providing log file encryption and a
command line tool to process encrypted logs.

%package doc
Summary: HTML documentation for rsyslog
BuildArch: noarch

%description doc
This subpackage contains documentation for rsyslog.

%package elasticsearch
Summary: ElasticSearch output module for rsyslog
Requires: %name = %version-%release
BuildRequires: libcurl-devel

%description elasticsearch
This module provides the capability for rsyslog to feed logs directly into
Elasticsearch.

%package mmjsonparse
Summary: JSON enhanced logging support
Requires: %name = %version-%release

%description mmjsonparse
This module provides the capability to recognize and parse JSON enhanced
syslog messages.

%package mysql
Summary: MySQL support for rsyslog
Requires: %name = %version-%release
BuildRequires: mariadb-connector-c-devel

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%package mmsnmptrapd
Summary: Message modification module for snmptrapd generated messages
Requires: %name = %version-%release

%description mmsnmptrapd
This message modification module takes messages generated from snmptrapd and
modifies them so that they look like they originated from the read originator.

%package mmaudit
Summary: Message modification module supporting Linux audit format
Requires: %name = %version-%release

%description mmaudit
This module provides message modification supporting Linux audit format
in various settings.

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Requires: %name = %version-%release
BuildRequires: krb5-devel

%description gssapi
The rsyslog-gssapi package contains the rsyslog plugins which support GSSAPI
authentication and secure connections. GSSAPI is commonly used for Kerberos
authentication.

%package gnutls
Summary: TLS protocol support for rsyslog via GnuTLS library
Requires: %name = %version-%release
BuildRequires: gnutls-devel

%description gnutls
The rsyslog-gnutls package contains the rsyslog plugins that provide the
ability to send and receive syslog messages via TCP or RELP using TLS
encryption via GnuTLS library. For details refer to rsyslog doc on imtcp
and omfwd modules.

%package udpspoof
Summary: Provides the omudpspoof module
Requires: %name = %version-%release
BuildRequires: libnet-devel

%description udpspoof
This module is similar to the regular UDP forwarder, but permits to
spoof the sender address. Also, it enables to circle through a number
of source ports.

%package_help

%prep
%setup -q -a 1 -T -c
mv build doc

%autosetup -n %{name}-%{version} -D -p1

%build
autoreconf -vfi

%ifarch sparc64
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DPATH_PIDFILE=\\\"%{Pidfile}\\\""
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DPATH_PIDFILE=\\\"%{Pidfile}\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

# the hiredis-devel package doesn't provide a pkg-config file
export HIREDIS_CFLAGS=-I/usr/include/hiredis
export HIREDIS_LIBS="-L%{_libdir} -lhiredis"
%configure \
	--prefix=/usr \
	--disable-static \
	--enable-testbench \
	--enable-elasticsearch \
	--enable-generate-man-pages \
	--enable-gnutls \
	--enable-gssapi-krb5 \
	--enable-imdiag \
	--enable-imfile \
        %if %{systemd_lived} == 1
        --enable-imjournal \
        --enable-omjournal \
        %endif
	--enable-impstats \
	--enable-imptcp \
	--enable-mail \
	--enable-mmanon \
	--enable-mmaudit \
	--enable-mmcount \
	--enable-mmkubernetes \
	--enable-mmjsonparse \
	--enable-mmnormalize \
	--enable-mmsnmptrapd \
	--enable-mysql \
	--enable-omamqp1 \
	--enable-omhiredis \
	--enable-ommongodb \
	--enable-omprog \
	--enable-omrabbitmq \
	--enable-omstdout \
	--enable-omudpspoof \
	--enable-omuxsock \
	--enable-pgsql \
	--enable-pmaixforwardedfrom \
	--enable-pmcisconames \
	--enable-pmlastmsg \
	--enable-pmsnare \
	--enable-relp \
	--enable-snmp \
	--enable-unlimited-select \
	--enable-usertools \
	--enable-omkafka

%make_build

%check
make V=1 check

%install
%make_install

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -d -m 755 $RPM_BUILD_ROOT%{_unitdir}
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/rsyslog.d
install -d -m 700 $RPM_BUILD_ROOT%{rsyslog_statedir}
install -d -m 700 $RPM_BUILD_ROOT%{rsyslog_pkidir}
install -d -m 755 $RPM_BUILD_ROOT%{rsyslog_docdir}/html

install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rsyslog
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/rsyslog
install -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_unitdir}/rsyslog.service
install -p -m 644 plugins/ommysql/createDB.sql $RPM_BUILD_ROOT%{rsyslog_docdir}/mysql-createDB.sql
install -p -m 644 plugins/ompgsql/createDB.sql $RPM_BUILD_ROOT%{rsyslog_docdir}/pgsql-createDB.sql
dos2unix tools/recover_qi.pl
install -p -m 644 tools/recover_qi.pl $RPM_BUILD_ROOT%{rsyslog_docdir}/recover_qi.pl

mkdir -p $RPM_BUILD_ROOT/etc/cron.d/
install -m 0600 %{_sourcedir}/timezone.cron $RPM_BUILD_ROOT/etc/cron.d/
install -m 0500 %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/os_rotate_and_save_log.sh
install -m 0500 %{SOURCE6} $RPM_BUILD_ROOT%{_bindir}/os_check_timezone_for_rsyslog.sh
install -m 0500 %{SOURCE9} $RPM_BUILD_ROOT%{_bindir}/timezone_update.sh

cp -r doc/* $RPM_BUILD_ROOT%{rsyslog_docdir}/html
rm -f %{buildroot}%{_libdir}/rsyslog/imdiag.so
rm -f %{buildroot}%{_libdir}/rsyslog/liboverride_getaddrinfo.so
rm -f %{buildroot}%{_libdir}/rsyslog/liboverride_gethostname.so
rm -f %{buildroot}%{_libdir}/rsyslog/liboverride_gethostname_nonfqdn.so
%delete_la

%pre

%post
for n in /var/log/{messages,secure,maillog,spooler}
do
	[ -f $n ] && continue
	umask 066 && touch $n
done

%if %{systemd_lived} == 1
%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
%systemd_postun_with_restart rsyslog.service

%endif

%files
%defattr(-,root,root,-)
%doc ChangeLog README.md
%license AUTHORS
%doc %{rsyslog_docdir}/pgsql-createDB.sql
%license COPYING*
%{rsyslog_docdir}
%dir %{_libdir}/rsyslog
%dir %{_sysconfdir}/rsyslog.d
%dir %{rsyslog_statedir}
%dir %{rsyslog_pkidir}
%{_sbindir}/rsyslogd
%attr(500,root,root) %{_bindir}/os_rotate_and_save_log.sh
%attr(500,root,root) %{_bindir}/os_check_timezone_for_rsyslog.sh
%attr(500,root,root) %{_bindir}/timezone_update.sh
/etc/cron.d/timezone.cron
%{_unitdir}/rsyslog.service
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/rsyslog
%{_libdir}/rsyslog/fmhttp.so
%{_libdir}/rsyslog/fmhash.so
%{_libdir}/rsyslog/imfile.so
%if %{systemd_lived} == 1
%{_libdir}/rsyslog/omjournal.so
%{_libdir}/rsyslog/imjournal.so
%endif
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/impstats.so
%{_libdir}/rsyslog/imptcp.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/mmanon.so
%{_libdir}/rsyslog/mmcount.so
%{_libdir}/rsyslog/mmexternal.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omstdout.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmaixforwardedfrom.so
%{_libdir}/rsyslog/pmcisconames.so
%{_libdir}/rsyslog/pmlastmsg.so
%{_libdir}/rsyslog/pmsnare.so
%exclude %{rsyslog_docdir}/html
%exclude %{rsyslog_docdir}/mysql-createDB.sql
%exclude %{rsyslog_docdir}/pgsql-createDB.sql

%files hiredis
%{_libdir}/rsyslog/omhiredis.so

%files kafka
%{_libdir}/rsyslog/omkafka.so

%files mmnormalize
%{_libdir}/rsyslog/mmnormalize.so

%files mmkubernetes
%{_libdir}/rsyslog/mmkubernetes.so

%files mongodb
%{_bindir}/logctl
%{_libdir}/rsyslog/ommongodb.so

%files omamqp1
%{_libdir}/rsyslog/omamqp1.so

%files pgsql
%doc %{rsyslog_docdir}/pgsql-createDB.sql
%{_libdir}/rsyslog/ompgsql.so

%files rabbitmq
%{_libdir}/rsyslog/omrabbitmq.so

%files relp
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/omrelp.so

%files snmp
%{_libdir}/rsyslog/omsnmp.so

%files crypto
%{_bindir}/rscryutil
%{_libdir}/rsyslog/lmcry_gcry.so

%files doc
%doc %{rsyslog_docdir}/html

%files elasticsearch
%{_libdir}/rsyslog/omelasticsearch.so

%files mmjsonparse
%{_libdir}/rsyslog/mmjsonparse.so

%files mysql
%doc %{rsyslog_docdir}/mysql-createDB.sql
%{_libdir}/rsyslog/ommysql.so

%files mmsnmptrapd
%{_libdir}/rsyslog/mmsnmptrapd.so

%files mmaudit
%{_libdir}/rsyslog/mmaudit.so

%files gssapi
%{_libdir}/rsyslog/lmgssutil.so
%{_libdir}/rsyslog/imgssapi.so
%{_libdir}/rsyslog/omgssapi.so

%files gnutls
%{_libdir}/rsyslog/lmnsd_gtls.so

%files udpspoof
%{_libdir}/rsyslog/omudpspoof.so

%files help
%doc %{rsyslog_docdir}/html
%{_mandir}/man5/rsyslog.conf.5.gz
%{_mandir}/man8/rsyslogd.8.gz
%{_mandir}/man1/rscryutil.1.gz

%changelog
* Mon Oct 10 2022 huangduirong <huangduirong@huawei.com> - 8.2110.0-11
- Type:NA
- ID:NA
- SUG:NA
- DESC:remove the sphinx-build in prep

* Thu Aug 04 2022 zhouwenpei <zhouwenpei1@h-partners.com> - 8.2110.0-10
- backport patches from upstream and enable check

* Mon May 23 2022 zhanghaolian <zhanghaolian@huawei.com> - 8.2110.0-9
- fix CVE-2022-24903

* Fri Mar 25 2022 wuchaochao <cyanrose@yeah.net> - 8.2110.0-8
- add systemd_lived macro

* Mon Mar 14 2022 wuchaochao <wuchaochao4@huawei.com> - 8.2110.0-7
- change startlimitburst spelling errors

* Feb Mon 28 2022  wangkerong <wangkerong@h-partners.com> - 8.2110.0-6
- Increase the limit on restart frequency

* Feb Mon 28 2022  wangkerong <wangkerong@h-partners.com> - 8.2110.0-5
- update timezone when restart rsyslog

* Wed Feb 23 2022  wuchaochao <wuchaochao4@huawei.com> - 8.2110.0-4
- delete  rsyslog-8.24.0-set-permission-of-syslogd-dot-pid-to-0644.patch

* Sat Feb 19 2022 liuyumeng <liuyumeng5@h-partners.com> - 8.2110.0-3
- print main queue info to journal

* Tue Dec 14 2021 wuchaochao <wuchaochao4@huawei.com> - 8.2110.0-2
- move rsyslog-crypto rsyslog-doc rsyslog-elasticsearch rsyslog-mmjsonparse syslog-mmaudit rsyslog-mmsnmptrapd rsyslog-mysql syslog-gssapi rsyslog-gnutls rsyslog-updspoof from rsyslog

* Thu Dec 09 2021 wuchaochao <wuchaochao4@huawei.com> - 8.2110.0-1
- update version to 8.2110.0

* Thu Aug 26 2021 wuchaochao <wuchaochao4@huawei.com> - 8.2012.0-4
- Type:NA
- ID:NA
- SUG:restart
- DESC:remove RSYSLOG_OPTIONS and change rsyslog.service files

* Wed Aug 25 2021 wuchaochao <wuchaochao4@huawei.com> - 8.2012.0-3
- Type:NA
- ID:NA
- SUG:restart
- DESC:add RSYSLOG_OPTIONS and organize rsyslog.service files

* Fri Jun 11 2021 shangyibin<shangyibin1@huawei.com> - 8.2012.0-2
- Type:NA
- ID:NA
- SUG:restart
- DESC:remove the dependence on libdbi

* Wed Feb 3 2021 yuanxin <yuanxin24@huawei.com> - 8.2012.0-1
- Upgrade version to 8.2012.0

* Thu Sep 15 2020 Guodong Zhu<zhuguodong8@huawei.com> - 8.2006.0-2
- Type:NA
- ID:NA
- SUG:restart
- DESC: fix potential file descriptor leak in one backport patch

* Mon Jul 27 2020 shixuantong<shixuantong@huawei.com> - 8.2006.0-1
- Type:NA
- ID:NA
- SUG:NA
- DESC:update to 8.2006-1

* Thu Apr 16 2020 Shouping Wang<wangshouping@huawei.com> - 8.2002.0-1
- Type: bugfix
- ID:NA
- SUG:restart
- DESC: upgrade rsyslog to 8.2002.0

* Wed Mar 25 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: the return value judgment of recv() is err in CheckConnection

* Tue Mar 24 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h4
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: parameter streamdriver.permitexpiredcerts did not work

* Thu Mar 19 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h3
- Type:bugfix
- ID:NA
- SUG:restart
- DESC: del imjournalRatelimitInterval and add *.emerg

* Sat Mar 7 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h2
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:emergency messages not to everyone

* Fri Mar 6 2020 Shouping Wang<wangshouping@huawei.com> - 8.1907.0-5.h1
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:create pid file

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.1907.0-5
- del unuse info

* Wed Nov 27 2019 chengquan <chengquan3@huawei.com> - 8.1907.0-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove useless install dependencies

* Fri Nov 8 2019 chengquan <chengquan3@huawei.com> - 8.1907.0-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add self-study patches

* Fri Oct 18 2019 chengquan <chengquan3@huawei.com> - 8.1907.0-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix spec rule in openeuler

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 8.1907.0-1
- Package init
