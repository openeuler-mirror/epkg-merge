#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1
cp %{SOURCE1} .
autoreconf -f -i

}

build() {
%configure %%{env.configureFlags} --sbindir=/sbin --libdir=/%{_lib} \
%ifarch %{golang_arches}
--with-golang \
%endif

make CFLAGS="%{optflags}" %{?_smp_mflags}

}

install() {
mkdir -p $RPM_BUILD_ROOT/{sbin,etc/audit/plugins.d,etc/audit/rules.d}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man5,man8}
mkdir -p $RPM_BUILD_ROOT/%{_lib}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/audit
mkdir -p --mode=0700 $RPM_BUILD_ROOT/%{_var}/log/audit
mkdir -p $RPM_BUILD_ROOT/%{_var}/spool/audit
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libaudit.a $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%{_lib}/libauparse.a $RPM_BUILD_ROOT%{_libdir}
curdir=`pwd`
cd $RPM_BUILD_ROOT/%{_libdir}
LIBNAME=`basename \`ls $RPM_BUILD_ROOT/%{_lib}/libaudit.so.1.*.*\``
ln -s ../../%{_lib}/$LIBNAME libaudit.so
LIBNAME=`basename \`ls $RPM_BUILD_ROOT/%{_lib}/libauparse.so.0.*.*\``
ln -s ../../%{_lib}/$LIBNAME libauparse.so
cd $curdir
rm -f $RPM_BUILD_ROOT/%{_lib}/libaudit.so
rm -f $RPM_BUILD_ROOT/%{_lib}/libauparse.so

find $RPM_BUILD_ROOT/%{_libdir}/python%{python3_version}/site-packages -name '*.a' -delete

mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig $RPM_BUILD_ROOT%{_libdir}

touch -r ./audit.spec $RPM_BUILD_ROOT/etc/libaudit.conf
touch -r ./audit.spec $RPM_BUILD_ROOT/usr/share/man/man5/libaudit.conf.5.gz

%delete_la

}

check() {
%ifarch %{golang_arches}
make check
%endif
rm -f rules/Makefile*

}

