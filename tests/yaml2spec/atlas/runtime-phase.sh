#!/usr/bash

post() {
%post -p /sbin/ldconfig
}

postun() {
%postun -p /sbin/ldconfig
}

posttrans:devel() {
/usr/sbin/alternatives --install %{_includedir}/atlas atlas-inc \
	%{_includedir}/atlas-%{_arch}-base %{pr_base}
}

postun:devel() {
if [ $1 -ge 0 ] ; then
    /usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-base
fi
}

%if "%{?enable_native_atlas}" == "0"
%ifarch x86_64

post:atlas-corei2() {
%post -n atlas-corei2 -p /sbin/ldconfig
}

postun:atlas-corei2() {
%postun -n atlas-corei2 -p /sbin/ldconfig
}

posttrans:corei2-devel() {
/usr/sbin/alternatives --install %{_includedir}/atlas atlas-inc     \
	%{_includedir}/atlas-%{_arch}-corei2  %{pr_corei2}
}

postun:corei2-devel() {
if [ $1 -ge 0 ] ; then
    /usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-corei2
fi
}

%endif
%endif
