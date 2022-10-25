#!/usr/bash

prep() {
%setup -q -a 3

pushd pam_ssh_agent_auth-pam_ssh_agent_auth-0.10.4
%patch3 -p2 -b .psaa-build
%patch4 -p2 -b .psaa-seteuid
%patch5 -p2 -b .psaa-visibility
%patch7 -p2 -b .psaa-compat
%patch6 -p2 -b .psaa-agent
%patch8 -p2 -b .psaa-deref
rm -f $(cat %{SOURCE4})
popd

%patch9 -p1 -b .role-mls
%patch10 -p1 -b .privsep-selinux
%patch11 -p1 -b .keycat
%patch12 -p1 -b .ip-opts
%patch13 -p1 -b .keyperm
%patch14 -p1 -b .ipv6man
%patch15 -p1 -b .sigpipe
%patch16 -p1 -b .x11
%patch18 -p1 -b .progress
%patch19 -p1 -b .grab-info
%patch20 -p1
%patch21 -p1 -b .log-usepam-no
%patch22 -p1 -b .evp-ctr
%patch23 -p1 -b .gsskex
%patch24 -p1 -b .force_krb
%patch26 -p1 -b .ccache_name
%patch27 -p1 -b .k5login
%patch28 -p1 -b .kuserok
%patch29 -p1 -b .fromto-remote
%patch30 -p1 -b .contexts
%patch31 -p1 -b .log-in-chroot
%patch32 -p1 -b .scp
%patch25 -p1 -b .GSSAPIEnablek5users
%patch33 -p1 -b .sshdt
%patch34 -p1 -b .sftp-force-mode
%patch35 -p1 -b .s390-dev
%patch36 -p1 -b .x11max
%patch37 -p1 -b .systemd
%patch38 -p1 -b .refactor
%patch39 -p1 -b .sandbox
%patch40 -p1 -b .pkcs11-uri
%patch41 -p1 -b .scp-ipv6
%patch42 -p1 -b .crypto-policies
%patch43 -p1 -b .openssl-evp
%patch44 -p1 -b .openssl-kdf
%patch45 -p1 -b .visibility
%patch46 -p1 -b .x11-ipv6
%patch47 -p1 -b .keygen-strip-doseol
%patch48 -p1 -b .preserve-pam-errors
%patch49 -p1 -b .kill-scp
%patch1 -p1 -b .audit
%patch2 -p1 -b .audit-race
%patch17 -p1 -b .fips
%patch0 -p1 -b .coverity

%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1

autoreconf
pushd pam_ssh_agent_auth-pam_ssh_agent_auth-0.10.4
autoreconf
popd

}

build() {
CFLAGS="$RPM_OPT_FLAGS -fvisibility=hidden"; export CFLAGS

CFLAGS="$CFLAGS -Os"
%ifarch s390 s390x sparc sparcv9 sparc64
CFLAGS="$CFLAGS -fPIC"
%else
CFLAGS="$CFLAGS -fpic"
%endif
SAVE_LDFLAGS="$LDFLAGS"
LDFLAGS="$LDFLAGS -pie -z relro -z now"

export CFLAGS
export LDFLAGS

if test -r /etc/profile.d/krb5-devel.sh ; then
source /etc/profile.d/krb5-devel.sh
fi
krb5_prefix=`krb5-config --prefix`
if test "$krb5_prefix" != "%{_prefix}" ; then
CPPFLAGS="$CPPFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"; export CPPFLAGS
CFLAGS="$CFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"
LDFLAGS="$LDFLAGS -L${krb5_prefix}/%{_lib}"; export LDFLAGS
else
krb5_prefix=
CPPFLAGS="-I%{_includedir}/gssapi"; export CPPFLAGS
CFLAGS="$CFLAGS -I%{_includedir}/gssapi"
fi

%configure \
    --sysconfdir=%{_sysconfdir}/ssh --libexecdir=%{_libexecdir}/openssh \
    --datadir=%{_datadir}/openssh \
    %%{env.configureFlags} \
%ifnarch riscv64
--with-sandbox=seccomp_filter \
%endif
--with-kerberos5${krb5_prefix:+=${krb5_prefix}} --with-libedit

make
gtk2=yes

pushd contrib
if [ $gtk2 = yes ] ; then
CFLAGS="$CFLAGS %{?__global_ldflags}" \
        make gnome-ssh-askpass2
mv gnome-ssh-askpass2 gnome-ssh-askpass
else
CFLAGS="$CFLAGS %{?__global_ldflags}"
make gnome-ssh-askpass1
mv gnome-ssh-askpass1 gnome-ssh-askpass
fi
popd

pushd pam_ssh_agent_auth-pam_ssh_agent_auth-0.10.4
LDFLAGS="$SAVE_LDFLAGS"
%configure --with-selinux --libexecdir=/%{_libdir}/security --with-mantype=man \
    --without-openssl-header-check
make
popd

}

check() {
%if %{?_with_check:1}%{!?_with_check:0}
make tests
%endif

}

install() {
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd

%make_install

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/sysconfig/
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m644 %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/ssh-keycat
install -m644 %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/sshd
install -m644 ssh_config_redhat $RPM_BUILD_ROOT/etc/ssh/ssh_config.d/05-redhat.conf
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/%{_unitdir}/sshd@.service
install -m644 %{SOURCE8} $RPM_BUILD_ROOT/%{_unitdir}/sshd.socket
install -m644 %{SOURCE9} $RPM_BUILD_ROOT/%{_unitdir}/sshd.service
install -m644 %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen@.service
install -m644 %{SOURCE13} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen.target
install -d -m755 $RPM_BUILD_ROOT/%{_userunitdir}
install -m644 %{SOURCE14} $RPM_BUILD_ROOT/%{_userunitdir}/ssh-agent.service
install -m744 %{SOURCE11} $RPM_BUILD_ROOT/%{_libexecdir}/openssh/sshd-keygen
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install -m644 -D %{SOURCE12} $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf
install contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass

ln -s gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

pushd pam_ssh_agent_auth-pam_ssh_agent_auth-0.10.4
make install DESTDIR=$RPM_BUILD_ROOT
popd

}

