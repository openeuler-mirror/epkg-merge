%global _python_bytecompile_extra 0
%bcond_with sandbox

Name:      policycoreutils
Version:   3.3
Release:   2
Summary:   Policy core utilities of selinux
License:   GPLv2
URL:       https://github.com/SELinuxProject
Source0:   https://github.com/SELinuxProject/selinux/archive/refs/tags/policycoreutils-%{version}.tar.gz
Source7:   selinux-autorelabel
Source8:   selinux-autorelabel.service
Source9:   selinux-autorelabel-mark.service
Source10:  selinux-autorelabel.target
Source11:  selinux-autorelabel-generator.sh

Patch0:    fix-fixfiles-N-date-function.patch
Patch1:    fix-fixfiles-N-date-function-two.patch 

BuildRequires: gcc
BuildRequires: pam-devel libsepol-static >= 3.3 libsemanage-static >= 3.3 libselinux-devel >= 3.3  libcap-devel audit-libs-devel  gettext
BuildRequires: desktop-file-utils dbus-devel dbus-glib-devel python3-devel libcap-ng-devel
BuildRequires: systemd systemd-units
Requires:      libsepol >= 3.3 libselinux-utils util-linux grep gawk diffutils rpm sed coreutils

Provides:      %{name}-restorecond = %{version}-%{release}
Obsoletes:     %{name}-restorecond < %{version}-%{release}
Provides:      %{name}-newrole = %{version}-%{release}
Obsoletes:     %{name}-newrole < %{version}-%{release}
Obsoletes:     python2-policycoreutils
Provides:      /sbin/fixfiles
Provides:      /sbin/restorecon

%description
It contains the selinux policy core utilities

%package -n python3-policycoreutils
Summary:   python3 utilities for seLinux policy core
%{?python_provide:%python_provide python3-policycoreutils}
Requires:  policycoreutils = %{version}-%{release}
Requires:  python3-libselinux python3-libsemanage >= 3.3
Requires:  audit-libs-python3 >= 2.8.5
Requires:  python3-IPy
Requires:  checkpolicy
Requires:  python3-setools >= 4.3.0
BuildArch: noarch

Provides:  %{name}-python3 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}

%description -n python3-policycoreutils
It contains the python3 policy core utilities for selinux

%package   python-utils
Summary:   Policy core python utilities for selinux
Requires:  python3-policycoreutils = %{version}-%{release}
Obsoletes: policycoreutils-python <= 2.4-4
BuildArch: noarch

%description python-utils
It contains the python utilities for selinux

%package   dbus
Summary:   Policy core DBUS for selinux
Requires:  python3-policycoreutils = %{version}-%{release} python3-slip-dbus
BuildArch: noarch

%description dbus
It contains policy core DBUS for selinux

%package   devel
Summary:   Policy core devel utilities for selinux
Requires:  policycoreutils-python-utils = %{version}-%{release}
Requires:  /usr/bin/make
Requires:  selinux-policy-devel

%description devel
It contains policy core devel utilities for selinux

%if %{with sandbox}
%package   sandbox
Summary:   Sandbox utilities for selinux
Requires:  python3-policycoreutils = %{version}-%{release}
Requires:  xorg-x11-server-Xephyr >= 1.14.1-2 /usr/bin/rsync /usr/bin/xmodmap
Requires:  openbox

%description sandbox
It contains sandbox utilities for selinux
%endif

%package   help
Summary:   Including man files for selinux
Requires:  man

%description help
This contains man files for the using of selinux.


%prep
%autosetup -p 1  -n selinux-policycoreutils-%{version}

%build
%set_build_flags
export PYTHON=%{__python3}

make -C policycoreutils LSPP_PRIV=y SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="%{_sbindir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C python  SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C semodule-utils  SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C restorecond     SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
%if %{with sandbox}
make -C sandbox SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
%endif
make -C dbus    SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all

%install
mkdir -p %{buildroot}/%{_defaultdocdir}/%{name}/
make -C policycoreutils LSPP_PRIV=y  DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" install
make -C python  PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make -C semodule-utils  PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
make -C restorecond     PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
%if %{with sandbox}
make -C sandbox PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install
%endif
make -C dbus    PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install


rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/restorecond
rm -f %{buildroot}/%{_sbindir}/open_init_pty
rm -f %{buildroot}/%{_sbindir}/run_init
rm -f %{buildroot}/%{_mandir}/man8/open_init_pty.8
rm -f %{buildroot}/%{_mandir}/ru/man8/run_init.8*
rm -f %{buildroot}/%{_mandir}/man8/run_init.8*
rm -f %{buildroot}/etc/pam.d/run_init*

rm -f  %{buildroot}%{python3_sitelib}/sepolicy/gui.*
rm -f  %{buildroot}%{python3_sitelib}/sepolicy/sepolicy.glade

install -m 644 -p %{SOURCE8} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE9} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE10} %{buildroot}/%{_unitdir}/
install -D -m 755 -p %{SOURCE11} %{buildroot}/%{_systemdgeneratordir}/%{basename:%{SOURCE11}}
install -m 755 -p %{SOURCE7} %{buildroot}/%{_libexecdir}/selinux/

pathfix.py -i "%{__python3} -Es" -p %{buildroot}%{python3_sitelib}
pathfix.py -i "%{__python3} -Es" -p %{buildroot}%{_sbindir}/semanage \
    %if %{with sandbox}
    %{buildroot}%{_bindir}/sandbox \
    %{buildroot}%{_datadir}/sandbox/start \
    %endif
    %{buildroot}%{_bindir}/chcat  %{buildroot}%{_bindir}/audit2allow \
    %{buildroot}%{_bindir}/sepolicy   %{buildroot}%{_bindir}/sepolgen-ifgen \
    %{buildroot}%{_datadir}/system-config-selinux/selinux_server.py


find %{buildroot}%{python3_sitelib} %{buildroot}%{python3_sitearch} \
    %{buildroot}%{_sbindir} %{buildroot}%{_bindir} %{buildroot}%{_datadir} -type f -name '*~' | xargs rm -f

%py_byte_compile %{__python3} %{buildroot}%{_datadir}/system-config-selinux

%find_lang policycoreutils

%post
%systemd_post selinux-autorelabel-mark.service restorecond.service

%preun
%systemd_preun selinux-autorelabel-mark.service restorecond.service

%postun
%systemd_postun_with_restart restorecond.service


%files -f %{name}.lang
%license policycoreutils/COPYING
%doc %{_usr}/share/doc/%{name}
%config(noreplace) %{_sysconfdir}/sestatus.conf
%config(noreplace) %{_sysconfdir}/pam.d/newrole
%config(noreplace) %{_sysconfdir}/selinux/restorecond.conf
%config(noreplace) %{_sysconfdir}/selinux/restorecond_user.conf
%{_sbindir}/*
%exclude %{_sbindir}/{seunshare,semanage}
%{_bindir}/secon
%{_bindir}/semodule_expand
%{_bindir}/semodule_link
%{_bindir}/semodule_package
%{_bindir}/semodule_unpackage
%{_bindir}/sestatus
%{_libexecdir}/selinux/hll
%dir %{_datadir}/bash-completion
%{_datadir}/bash-completion/completions/setsebool
%{_unitdir}/restorecond.service
%{_userunitdir}/restorecond_user.service
%{_sysconfdir}/xdg/autostart/restorecond.desktop
%{_datadir}/dbus-1/services/org.selinux.Restorecond.service
%attr(0755,root,root) %caps(cap_dac_read_search,cap_setpcap,cap_audit_write,cap_sys_admin,cap_fowner,cap_chown,cap_dac_override=pe) %{_bindir}/newrole
%{_libexecdir}/selinux/selinux-autorelabel
%{_unitdir}/selinux-autorelabel-mark.service
%{_unitdir}/selinux-autorelabel.service
%{_unitdir}/selinux-autorelabel.target
%{_systemdgeneratordir}/selinux-autorelabel-generator.sh

%files python-utils
%{_bindir}/audit2allow
%{_bindir}/audit2why
%{_sbindir}/semanage
%{_bindir}/chcat
%if %{with sandbox}
%{_bindir}/sandbox
%endif
%{_sysconfdir}/dbus-1/system.d/org.selinux.conf
%{_datadir}/bash-completion/completions/semanage

%files dbus
%{_datadir}/system-config-selinux/selinux_server.py
%{_datadir}/polkit-1/actions/org.selinux.policy
%{_sysconfdir}/dbus-1/system.d/org.selinux.conf
%{_datadir}/dbus-1/system-services/org.selinux.service
%dir %{_datadir}/system-config-selinux/__pycache__
%{_datadir}/system-config-selinux/__pycache__/selinux_server.*

%files -n python3-policycoreutils
%{python3_sitelib}/__pycache__
%{python3_sitelib}/sepolgen
%dir %{python3_sitelib}/sepolicy
%{python3_sitelib}/sepolicy/templates
%dir %{python3_sitelib}/sepolicy/help
%{python3_sitelib}/sepolicy/help/*
%{python3_sitelib}/sepolicy/__init__.py*
%{python3_sitelib}/sepolicy/__pycache__
%{python3_sitelib}/sepolicy/manpage.py*
%{python3_sitelib}/sepolicy/network.py*
%{python3_sitelib}/sepolicy/transition.py*
%{python3_sitelib}/sepolicy/sedbus.py*
%{python3_sitelib}/sepolicy*.egg-info
%{python3_sitelib}/sepolicy/booleans.py*
%{python3_sitelib}/sepolicy/communicate.py*
%{python3_sitelib}/sepolicy/generate.py*
%{python3_sitelib}/sepolicy/interface.py*
%{python3_sitelib}/seobject.py*

%files devel
%{_bindir}/sepolicy
%{_bindir}/sepolgen
%{_bindir}/sepolgen-*
%{_usr}/share/bash-completion/completions/sepolicy
%dir  /var/lib/sepolgen
/var/lib/sepolgen/perm_map

%if %{with sandbox}
%files sandbox
%config(noreplace) %{_sysconfdir}/sysconfig/sandbox
%{_datadir}/sandbox/{start,sandboxX.sh}
%caps(cap_setpcap,cap_setuid,cap_fowner,cap_dac_override,cap_sys_admin,cap_sys_nice=pe) %{_sbindir}/seunshare
%endif

%files help
%{_mandir}/*

%changelog
* Thu Jun 30 2022 lujie <lujie54@huawei.com> - 3.3-2
- update policycoreutils tar.gz

* Thu Feb 17 2022 panxiaohe <panxh.life@foxmail.com> - 3.3-1
- update to 3.3

* Tue Sep 7 2021 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 3.1-8
- add "%%set_build_flags" for security build flags

* Fri Jun 4 2021 panxiaohe <panxiaohe@huawei.com> - 3.1-7
- add gcc to BuildRequires
- fix fixfiles -N date function
 
* Sun Dec 13 2020 luhuaxin <1539327763@qq.com> - 3.1-6
- add obsoletes of python2-policycoreutils

* Tue Dec 1 2020 Liquor <lirui130@huawei.com> - 3.1-5
- add the necessary version dependencies

* Mon Nov 30 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.1-4
- add version require of libsepol

* Mon Nov 2 2020 yixiangzhike <zhangxingliang3@huawei.com> - 3.1-3
- add selinux-autorelabel-mark.service to systemd_preun and systemd_post

* Thu Oct 29 2020 Hugel <gengqihu1@huawei.com> - 3.1-2
- remove the dependency on python2

* Fri Jul 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.1-1
- update to 3.1

* Thu Mar 5 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.8-14
- Build without sandbox

* Mon Feb 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.8-13
- Add unpackaged files

* Fri Feb 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.8-12
- Add selinux-autorelabel

* Fri Dec 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.8-11
- Simplify functions

* Fri Dec 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.8-10
- Delete unused patch

* Wed Sep 11 2019 zhanghaibo <ted.zhang@huawei.com> - 2.8-9
- Package init
