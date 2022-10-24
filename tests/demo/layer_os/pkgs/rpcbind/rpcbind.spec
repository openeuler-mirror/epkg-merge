%global rpcbind_user_group rpc
%global rpcbind_state_dir %{_rundir}/rpcbind

Name:              rpcbind
Version:           1.2.6
Release:           4
Summary:           Universal addresses to RPC program number mapper
License:           BSD

URL:               https://nfsv4.bullopensource.org
Source0:           https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:	   %{name}.sysconfig

Requires:	   glibc-common setup
Conflicts: 	   man-pages < 2.43-12
BuildRequires: 	   automake autoconf libtool systemd-devel
BuildRequires: 	   libtirpc-devel quota-devel systemd
Requires(pre):     coreutils shadow-utils
Requires(post):    chkconfig systemd
Requires(preun):   systemd
Requires(postun):  systemd coreutils

Patch100: 	   %{name}-0.2.3-systemd-envfile.patch
Patch101: 	   %{name}-0.2.3-systemd-tmpfiles.patch
Patch102: 	   %{name}-0.2.4-runstatdir.patch
Patch103: 	   %{name}-0.2.4-systemd-service.patch
Patch104: 	   %{name}-0.2.4-systemd-rundir.patch
Patch105:          bugfix-rpcbind-GETADDR-return-client-ip.patch
Patch6001: 	   CVE-2017-8779.patch
Patch6002: 	   backport-fix-double-free-in-init_transport.patch
Patch6003:         backport-debian-enable-rmt-calls-with-r.patch
Patch9000: 	   bugfix-listen-tcp-port-111.patch

Provides: 	   portmap = %{version}-%{release}
Obsoletes: 	   portmap <= 4.0-65.3

%description
The %{name} utility is a server that converts RPC program 
numbers into universal addresses. It must be running on the 
host to be able to make RPC calls on a server on that machine.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1 

%build
autoreconf -fisv
%configure  --enable-warmstarts  --with-statedir="%rpcbind_state_dir" \
    --with-rpcuser="%rpcbind_user_group"  --with-nss-modules="files altfiles" \
    --sbindir=%{_bindir}  --enable-debug --enable-rmtcalls

make all

%install
install -m 0755 -d %{buildroot}{%{_sbindir},%{_bindir},/etc/sysconfig}
install -m 0755 -d %{buildroot}%{_unitdir}
install -m 0755 -d %{buildroot}%{_tmpfilesdir}
install -m 0755 -d %{buildroot}%{_mandir}/man8
install -m 0755 -d %{buildroot}%{rpcbind_state_dir}
%make_install
make DESTDIR=$RPM_BUILD_ROOT install

install -m 644 %{SOURCE1} %{buildroot}/etc/sysconfig/%{name}

cd %{buildroot}%{_sbindir}
ln -sf ../bin/%{name}
ln -sf ../bin/rpcinfo

%pre
getent group rpc >/dev/null || groupadd -f -g 32 -r rpc
if ! getent passwd rpc >/dev/null ; then
	if ! getent passwd 32 >/dev/null ; then
	   useradd -l -c "Rpcbind Daemon" -d /var/lib/%{name}  \
	      -g rpc -M -s /sbin/nologin -o -u 32 rpc > /dev/null 2>&1
	else
	   useradd -l -c "Rpcbind Daemon" -d /var/lib/%{name}  \
	      -g rpc -M -s /sbin/nologin rpc > /dev/null 2>&1
	fi
fi

%post
%systemd_post %{name}.service %{name}.socket

%preun
%systemd_preun %{name}.service %{name}.socket

%postun
%systemd_postun_with_restart %{name}.service %{name}.socket

%triggerun -- %{name} < 0.2.0-15
%{_bindir}/systemd-sysv-convert --save %{name} >/dev/null 2>&1 ||:
/bin/systemctl --no-reload enable %{name}.service >/dev/null 2>&1
/sbin/chkconfig --del %{name} >/dev/null 2>&1 || :
/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :

%triggerin -- %{name} > 0.2.2-2.0
if systemctl -q is-enabled %{name}.socket
then
	/bin/systemctl reenable %{name}.socket  >/dev/null 2>&1 || :
	/bin/systemctl restart %{name}.socket >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/%{name}
%doc AUTHORS
%license COPYING
%{_sbindir}/*
%{_bindir}/*
%{_unitdir}/%{name}.*
%{_tmpfilesdir}/%{name}.conf
%attr(0700, %{rpcbind_user_group}, %{rpcbind_user_group}) %dir %{rpcbind_state_dir}

%files help
%defattr(-,root,root)
%doc ChangeLog README
%{_mandir}/man8/*.8.gz

%changelog
* Wed Mar 30 2022 kircher <majun65@huawei.com> - 1.2.6-4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:enable rmt-calls with -r

* Mon Feb 28 2022 quanhongfei <quanhongfei@h-partners.com> - 1.2.6-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix double free in init_transport

* Wed Feb 09 2022 yanglu <yanglu72@huawei.com> - 1.2.6-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:modify the getaddr method of ip

* Fri Dec 03 2021 quanhongfei <quanhongfei@huawei.com> - 1.2.6-1
- Type:requirements
- Id:NA
- SUG:NA
- DESC:update rpcbind to 1.2.6

* Thu Oct 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.2.5-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add copying file to rpcbind package

* Tue Sep 17 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.2.5-1
- Package init
