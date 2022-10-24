#!/usr/bash

prep() {
%autosetup -n Linux-PAM-%{version} -p1
cp %{SOURCE8} .
autoreconf -i

}

build() {
%configure \
	%%{env.configureFlags} \
	--libdir=%{_pamlibdir} \
	--includedir=%{_includedir}/security \

make -C po update-gmo
%make_build

}

install() {
%make_install

mkdir -p doc/README.d
for readme in modules/pam_*/README ; do
cp -f ${readme} doc/README.d/README.`dirname ${readme} | sed -e 's@^modules/@@'`
done

ln -sf pam_sepermit.so $RPM_BUILD_ROOT%{_moduledir}/pam_selinux_permit.so

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/Linux-PAM
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/environment

install -d -m 755 $RPM_BUILD_ROOT%{_pamconfdir}

install -m 644 -D modules/pam_namespace/pam_namespace.service \
  %{buildroot}%{_unitdir}/pam_namespace.service

install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_pamconfdir}/other
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_pamconfdir}/system-auth
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_pamconfdir}/password-auth
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_pamconfdir}/config-util
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_pamconfdir}/postlogin
install -m 600 /dev/null $RPM_BUILD_ROOT%{_secconfdir}/opasswd
install -d -m 755 $RPM_BUILD_ROOT/var/log
install -m 600 /dev/null $RPM_BUILD_ROOT/var/log/tallylog
install -d -m 755 $RPM_BUILD_ROOT/var/run/faillock

for phase in auth acct passwd session ; do
ln -sf pam_unix.so $RPM_BUILD_ROOT%{_moduledir}/pam_unix_${phase}.so
done

install -m644 -D %{SOURCE6} $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/pam.conf

find $RPM_BUILD_ROOT -type f -name "*.la" -delete -print
rm -fr $RPM_BUILD_ROOT/usr/share/doc/pam

%find_lang Linux-PAM

}

check() {
make check

}

