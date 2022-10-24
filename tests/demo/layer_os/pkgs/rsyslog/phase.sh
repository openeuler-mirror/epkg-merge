#!/usr/bash

prep() {
%setup -q -a 1 -T -c
mv build doc

%autosetup -n %{name}-%{version} -D -p1

}

build() {
autoreconf -vfi

%ifarch sparc64
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DPATH_PIDFILE=\\\"%{Pidfile}\\\""
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DPATH_PIDFILE=\\\"%{Pidfile}\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

export HIREDIS_CFLAGS=-I/usr/include/hiredis
export HIREDIS_LIBS="-L%{_libdir} -lhiredis"
%configure \
	--prefix=/usr \
	%%{env.configureFlags} \
%if %{systemd_lived} == 1
--enable-imjournal \
        --enable-omjournal \
        %endif

%make_build

%endif
}

check() {
make V=1 check

}

install() {
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

}

