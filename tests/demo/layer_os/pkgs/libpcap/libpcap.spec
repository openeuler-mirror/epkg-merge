Name:		libpcap
Epoch:    	14
Version:	1.10.1
Release:	2
Summary:	A system-independent interface for user-level packet capture
License:	BSD
URL:		http://www.tcpdump.org
Source0:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz

Patch0:         0003-pcap-linux-apparently-ctc-interfaces-on-s390-has-eth.patch
Patch1:         pcap-config-mitigate-multilib-conflict.patch

BuildRequires:	bison flex gcc glibc-kernheaders >= 2.2.0

%ifnarch i686
BuildRequires: bluez-libs-devel
%endif

%description
This is the official web site of tcpdump, a powerful command-line 
packet analyzer; and libpcap, a portable C/C++ library for 
network traffic capture.

%package 	devel
Summary:	header files for libpcap
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description	devel
header files for libpcap

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure
%make_build

%install
%make_install 

%delete_la_and_a

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libpcap.so.*

%files 	        devel
%defattr(-,root,root)
%{_bindir}/pcap-config
%{_includedir}/*
%{_libdir}/libpcap.so
%{_libdir}/pkgconfig/libpcap.pc

%files		help
%defattr(-,root,root)
%doc README.md CHANGES CREDITS
%{_mandir}/man*

%changelog
* Fri Feb 18 2022 xihaochen <xihaochen@h-partners.com> - 14:1.10.1-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: delete the bluez-libs-devel in i686 arch

* Thu Sep 16 2021 xinghe <xinghe2@huawei.com> - 14:1.10.1-1
- DESC:upgrade to 1.10.1

* Mon Aug 09 2021 yanglu <yanglu72@huawei.com> - 14:1.9.1-8
- DESC:delete -S git from %autosetup,and delete Buildrequires git

* Sat Nov 28 2020 xiaqirong <xiaqirong1@huawei.com> - 14:1.9.1-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:mitigate pcap config multilib conflict

* Fri Aug 07 2020 lunankun <lunankun@huawei.com> - 14:1.9.1-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix overflow in opt_init

* Tue May 26 2020 gaihuiying <gaihuiying1@huawei.com> - 14:1.9.1-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix overflow in opt_init

* Sat Jan 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 14:1.9.1-4
- delete useless info

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 14:1.9.1-3
- Package init
