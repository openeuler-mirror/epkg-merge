%global gtk2 1
%global pie 1

# Add option to build without GTK2 for older platforms with only GTK+.
# rpm -ba|--rebuild --define 'no_gtk2 1'
%{?no_gtk2:%global gtk2 0}

%global sshd_uid    74
%global openssh_release 6

Name:           openssh
Version:        8.8p1
Release:        %{openssh_release}
URL:            http://www.openssh.com/portable.html
License:        BSD
Summary:        An open source implementation of SSH protocol version 2

Source0:        https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1:        https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.asc
Source2:        sshd.pam
Source4:        http://prdownloads.sourceforge.net/pamsshagentauth/pam_ssh_agent_auth/pam_ssh_agent_auth-0.10.4.tar.gz
Source5:        pam_ssh_agent-rmheaders
Source6:        ssh-keycat.pam
Source7:        sshd.sysconfig
Source9:        sshd@.service
Source10:       sshd.socket
Source11:       sshd.service
Source12:       sshd-keygen@.service
Source13:       sshd-keygen
Source14:	sshd.tmpfiles
Source15:       sshd-keygen.target
Source16:	ssh-agent.service
Patch0:         openssh-6.7p1-coverity.patch
Patch1:         openssh-7.6p1-audit.patch
Patch2:         openssh-7.1p2-audit-race-condition.patch
Patch3:         pam_ssh_agent_auth-0.9.3-build.patch
Patch4:         pam_ssh_agent_auth-0.10.3-seteuid.patch
Patch5:         pam_ssh_agent_auth-0.9.2-visibility.patch
Patch6:         pam_ssh_agent_auth-0.9.3-agent_structure.patch
Patch7:         pam_ssh_agent_auth-0.10.2-compat.patch
Patch8:         pam_ssh_agent_auth-0.10.2-dereference.patch
Patch9:         openssh-7.8p1-role-mls.patch
Patch10:        openssh-6.6p1-privsep-selinux.patch
Patch12:        openssh-6.6p1-keycat.patch
Patch13:        openssh-6.6p1-allow-ip-opts.patch
Patch14:        openssh-6.6p1-keyperm.patch
Patch15:        openssh-5.9p1-ipv6man.patch
Patch16:        openssh-5.8p2-sigpipe.patch
Patch17:        openssh-7.2p2-x11.patch
Patch18:        openssh-7.7p1-fips.patch
Patch19:        openssh-5.1p1-askpass-progress.patch
Patch20:        openssh-4.3p2-askpass-grab-info.patch
Patch21:        openssh-7.7p1.patch
Patch22:        openssh-7.8p1-UsePAM-warning.patch
Patch23:        openssh-6.3p1-ctr-evp-fast.patch
Patch26:        openssh-8.0p1-gssapi-keyex.patch
Patch27:        openssh-6.6p1-force_krb.patch
Patch28:        openssh-6.6p1-GSSAPIEnablek5users.patch
Patch29:        openssh-7.7p1-gssapi-new-unique.patch
Patch30:        openssh-7.2p2-k5login_directory.patch
Patch31:        openssh-6.6p1-kuserok.patch
Patch32:        openssh-6.4p1-fromto-remote.patch
Patch33:        openssh-6.6.1p1-selinux-contexts.patch
Patch34:        openssh-6.6.1p1-log-in-chroot.patch
Patch35:        openssh-6.6.1p1-scp-non-existing-directory.patch
Patch36:        openssh-6.8p1-sshdT-output.patch
Patch37:        openssh-6.7p1-sftp-force-permission.patch
Patch38:        openssh-7.2p2-s390-closefrom.patch
Patch39:        openssh-7.3p1-x11-max-displays.patch
Patch40:        openssh-7.4p1-systemd.patch
Patch41:        openssh-7.6p1-cleanup-selinux.patch
Patch42:        openssh-7.5p1-sandbox.patch
Patch43:        openssh-8.0p1-pkcs11-uri.patch
Patch44:        openssh-7.8p1-scp-ipv6.patch
Patch46:        openssh-8.0p1-crypto-policies.patch
Patch47:        openssh-8.0p1-openssl-evp.patch
Patch48:        openssh-8.0p1-openssl-kdf.patch
Patch49:        openssh-8.2p1-visibility.patch
Patch50:	openssh-8.2p1-x11-without-ipv6.patch
Patch51:	openssh-8.0p1-keygen-strip-doseol.patch
Patch52:	openssh-8.0p1-preserve-pam-errors.patch
Patch53:	openssh-8.7p1-scp-kill-switch.patch

Patch54:        bugfix-sftp-when-parse_user_host_path-empty-path-should-be-allowed.patch
Patch55:        bugfix-openssh-6.6p1-log-usepam-no.patch
Patch56:        bugfix-openssh-add-option-check-username-splash.patch
Patch57:        feature-openssh-7.4-hima-sftpserver-oom-and-fix.patch
Patch58:        bugfix-openssh-fix-sftpserver.patch
Patch59:        set-sshd-config.patch
Patch60:	feature-add-SMx-support.patch

Requires:       /sbin/nologin
Requires:       libselinux >= 2.3-5 audit-libs >= 1.0.8
Requires:       openssh-server = %{version}-%{release}

BuildRequires:  gtk2-devel libX11-devel openldap-devel autoconf automake perl-interpreter perl-generators
BuildRequires:  zlib-devel audit-libs-devel >= 2.0.5 util-linux groff pam-devel
BuildRequires:  openssl-devel >= 0.9.8j perl-podlators systemd-devel gcc p11-kit-devel krb5-devel
BuildRequires:  libedit-devel ncurses-devel libselinux-devel >= 2.3-5 audit-libs >= 1.0.8 xauth gnupg2

Recommends:     p11-kit

%package        clients
Summary:        An open source SSH client applications
Requires:       openssh = %{version}-%{release}
Requires:       crypto-policies >= 20180306-1

%package        server
Summary:        An open source SSH server daemon
Requires:       openssh = %{version}-%{release}
Requires(pre):  shadow
Requires:       pam >= 1.0.1-3
Requires:       crypto-policies >= 20180306-1
%{?systemd_requires}

%package        keycat
Summary:        A mls keycat backend for openssh
Requires:       openssh = %{version}-%{release}

%package        askpass
Summary:        A passphrase dialog for OpenSSH and X
Requires:       openssh = %{version}-%{release}

%package -n pam_ssh_agent_auth
Summary:        PAM module for authentication with ssh-agent
Version:        0.10.4
Release:        4.%{openssh_release}
License:        BSD

%description
OpenSSH is the premier connectivity tool for remote login with the SSH protocol. \
It encrypts all traffic to eliminate eavesdropping, connection hijacking, and \
other attacks. In addition, OpenSSH provides a large suite of secure tunneling \
capabilities, several authentication methods, and sophisticated configuration options.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server.

%description keycat
OpenSSH mls keycat is backend for using the authorized keys in the
openssh in the mls mode.

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%description -n pam_ssh_agent_auth
Provides PAM module for the use of authentication with ssh-agent. Through the use of the\
forwarding of ssh-agent connection it also allows to authenticate with remote ssh-agent \
instance. The module is most useful for su and sudo service stacks.

%package_help

%prep
%setup -q -a 4

pushd pam_ssh_agent_auth-pam_ssh_agent_auth-0.10.4
%patch3 -p2 -b .psaa-build
%patch4 -p2 -b .psaa-seteuid
%patch5 -p2 -b .psaa-visibility
%patch7 -p2 -b .psaa-compat
%patch6 -p2 -b .psaa-agent
%patch8 -p2 -b .psaa-deref
# Remove duplicate headers and library files
rm -f $(cat %{SOURCE5})
popd

%patch9 -p1 -b .role-mls
%patch10 -p1 -b .privsep-selinux
%patch12 -p1 -b .keycat
%patch13 -p1 -b .ip-opts
%patch14 -p1 -b .keyperm
%patch15 -p1 -b .ipv6man
%patch16 -p1 -b .sigpipe
%patch17 -p1 -b .x11
%patch19 -p1 -b .progress
%patch20 -p1 -b .grab-info
%patch21 -p1
%patch22 -p1 -b .log-usepam-no
%patch23 -p1 -b .evp-ctr
%patch26 -p1 -b .gsskex
%patch27 -p1 -b .force_krb
%patch29 -p1 -b .ccache_name
%patch30 -p1 -b .k5login
%patch31 -p1 -b .kuserok
%patch32 -p1 -b .fromto-remote
%patch33 -p1 -b .contexts
%patch34 -p1 -b .log-in-chroot
%patch35 -p1 -b .scp
%patch28 -p1 -b .GSSAPIEnablek5users
%patch36 -p1 -b .sshdt
%patch37 -p1 -b .sftp-force-mode
%patch38 -p1 -b .s390-dev
%patch39 -p1 -b .x11max
%patch40 -p1 -b .systemd
%patch41 -p1 -b .refactor
%patch42 -p1 -b .sandbox
%patch43 -p1 -b .pkcs11-uri
%patch44 -p1 -b .scp-ipv6
%patch46 -p1 -b .crypto-policies
%patch47 -p1 -b .openssl-evp
%patch48 -p1 -b .openssl-kdf
%patch49 -p1 -b .visibility
%patch50 -p1 -b .x11-ipv6
%patch51 -p1 -b .keygen-strip-doseol
%patch52 -p1 -b .preserve-pam-errors
%patch53 -p1 -b .kill-scp
%patch1 -p1 -b .audit
%patch2 -p1 -b .audit-race
%patch18 -p1 -b .fips
%patch0 -p1 -b .coverity

%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1

autoreconf
pushd pam_ssh_agent_auth-pam_ssh_agent_auth-0.10.4
autoreconf
popd

%build
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
    --datadir=%{_datadir}/openssh --with-default-path=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin \
    --with-superuser-path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin \
    --with-privsep-path=%{_var}/empty/sshd --disable-strip \
    --without-zlib-version-check --with-ssl-engine --with-ipaddr-display \
    --with-pie=no --without-hardening --with-systemd --with-default-pkcs11-provider=yes \
    --with-pam --with-selinux --with-audit=linux --with-security-key-buildin=yes \
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

%check
#to run tests use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
make tests
%endif

%install
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd

%make_install

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/sysconfig/
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m644 %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/ssh-keycat
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/sshd
install -m644 ssh_config_redhat $RPM_BUILD_ROOT/etc/ssh/ssh_config.d/05-redhat.conf
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -m644 %{SOURCE9} $RPM_BUILD_ROOT/%{_unitdir}/sshd@.service
install -m644 %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}/sshd.socket
install -m644 %{SOURCE11} $RPM_BUILD_ROOT/%{_unitdir}/sshd.service
install -m644 %{SOURCE12} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen@.service
install -m644 %{SOURCE15} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen.target
install -d -m755 $RPM_BUILD_ROOT/%{_userunitdir}
install -m644 %{SOURCE16} $RPM_BUILD_ROOT/%{_userunitdir}/ssh-agent.service
install -m744 %{SOURCE13} $RPM_BUILD_ROOT/%{_libexecdir}/openssh/sshd-keygen
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install -m644 -D %{SOURCE14} $RPM_BUILD_ROOT%{_tmpfilesdir}/%{name}.conf
install contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass

ln -s gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

pushd pam_ssh_agent_auth-pam_ssh_agent_auth-0.10.4
make install DESTDIR=$RPM_BUILD_ROOT
popd

%pre
getent group ssh_keys >/dev/null || groupadd -r ssh_keys || :

%pre server
getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :

%post server
%systemd_post sshd.service sshd.socket

%preun server
%systemd_preun sshd.service sshd.socket

%postun server
%systemd_postun_with_restart sshd.service

%files
%license LICENCE
%doc CREDITS README.platform
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%attr(2555,root,ssh_keys) %{_libexecdir}/openssh/ssh-keysign

%files clients
%attr(0755,root,root) %{_bindir}/ssh
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config.d/05-redhat.conf
%attr(0755,root,root) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-sk-helper
%attr(0755,root,root) %{_userunitdir}/ssh-agent.service

%files server
%dir %attr(0711,root,root) %{_var}/empty/sshd
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0755,root,root) %{_libexecdir}/openssh/sshd-keygen
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0644,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0640,root,root) %config(noreplace) /etc/sysconfig/sshd
%attr(0644,root,root) %{_unitdir}/sshd.service
%attr(0644,root,root) %{_unitdir}/sshd@.service
%attr(0644,root,root) %{_unitdir}/sshd.socket
%attr(0644,root,root) %{_unitdir}/sshd-keygen@.service
%attr(0644,root,root) %{_unitdir}/sshd-keygen.target
%attr(0644,root,root) %{_tmpfilesdir}/openssh.conf

%files keycat
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-keycat
%attr(0644,root,root) %config(noreplace) /etc/pam.d/ssh-keycat

%files askpass
%attr(0644,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass

%files -n pam_ssh_agent_auth
%license pam_ssh_agent_auth-pam_ssh_agent_auth-0.10.4/OPENSSH_LICENSE
%attr(0755,root,root) %{_libdir}/security/pam_ssh_agent_auth.so

%files help
%doc ChangeLog OVERVIEW PROTOCOL* README README.privsep README.tun README.dns TODO
%doc HOWTO.ssh-keycat
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh*.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man5/ssh*.5*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/ssh*.8*
%attr(0644,root,root) %{_mandir}/man8/pam_ssh_agent_auth.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*

%changelog
* Thu Sep 01 2022 duyiwei<duyiwei@kylinos.cn> - 8.8P1-6
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:enable "include /etc/ssh/sshd_config.d/*.config" again

* Fri Jul 29 2022 kircher<majun65@huawei.com> - 8.8p1-5
- Type:bugfix
- CVE:Na
- SUG:NA
- DESC:add SMx support in openssh

* Thu May 05 2022 seuzw<930zhaowei@163.com> - 8.8p1-4
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:fix incorrect sftp-server binary path in /etc/ssh/sshd_config

* Wed Mar 09 2022 duyiwei<duyiwei@kylinos.cn> - 8.8P1-3
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:enable "include /etc/ssh/sshd_config.d/*.config"

* Mon Mar 07 2022 kircher<majun65@huawei.com> - 8.8P1-2
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:add sshd.tmpfiles

* Thu Oct 28 2021 kircher<kircherlike@outlook.com> - 8.8P1-1
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:update to openssh-8.8p1

* Fri Oct 8 2021 renmingshuai<renmingshuai@hauwei.com> - 8.2P1-15
- Type:cves
- CVE:CVE-2021-41617
- SUG:NA
- DESC:fix CVE-2021-41617

* Sat Sep 18 2021 kircher<kircherlike@outlook.com> - 8.2P1-14
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:backport patch from github to fix NULL ref

* Fri Jul 30 2021 kircher<majun65@huawei.com> - 8.2P1-13
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:remove debug message from sigchld handler

* Tue Jul 20 2021 seuzw<930zhaowei@163.com> - 8.2P1-12
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:move closefrom to before first malloc

* Fri Jul 09 2021 panchenbo<panchenbo@uniontech.com> - 8.2P1-11
- fix pam_ssh_agent_auth.8.gz conflicts

* Thu May 20 2021 seuzw<930zhaowei@163.com> - 8.2P1-10
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:add strict-scp-check for check command injection

* Mon Jan 4 2021 chxssg<chxssg@qq.com> - 8.2P1-9
- Type:cves
- CVE:CVE-2020-14145
- SUG:NA
- DESC:fix CVE-2020-14145

* Wed Nov 18 2020 gaihuiying<gaihuiying1@huawei.com> - 8.2P1-8
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:adjust pam_ssh_agent_auth release number

* Tue Nov 17 2020 gaihuiying<gaihuiying1@huawei.com> - 8.2P1-7
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:keep pam_ssh_agent_auth change release number with openssh

* Tue Sep 15 2020 liulong<liulong20@huawei.com> - 8.2P1-6
- Type:cves
- ID:CVE-2018-15919
- SUG:NA
- DESC:Fix CVE-2018-15919

* Thu Jul 2 2020 zhouyihang<zhouyihang3@huawei.com> - 8.2P1-5
- Type:cves
- ID:CVE-2020-12062
- SUG:NA
- DESC:Fix CVE-2020-12062

* Tue Jun 9 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.2P1-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add requires for openssh-server in openssh

* Wed May 6 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.2P1-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix update problem

* Sat Apr 18 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.2P1-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix pre problem

* Thu Apr 16 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.2P1-1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:update to 8.2P1

* Mon Mar 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.8P1-12
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:move sshd.service in %post server

* Wed Mar 18 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.8P1-11
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:reduction of authority

* Fri Mar 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.8P1-10
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:separate package

* Thu Mar 5 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.8P1-9
- Type:cves
- ID:CVE-2018-15919
- SUG:NA
- DESC:Fix CVE-2018-15919

* Thu Mar 5 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.8P1-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:debug3 to verbose in command line

* Tue Jan 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 7.8P1-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add the patch for bugfix

* Mon Dec 23 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.8P1-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:delete the patch

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.8P1-5
- Type:cves
- ID:NA
- SUG:restart
- DESC:fix cves

* Fri Sep 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.8p1-4
- Package init
