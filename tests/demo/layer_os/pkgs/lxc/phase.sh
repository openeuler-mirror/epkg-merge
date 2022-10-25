#!/usr/bash

prep() {
%autosetup -n lxc-4.0.3 -Sgit -p1

}

build() {
%configure %%{env.configureFlags} --docdir=%{_pkgdocdir}

%{make_build}

}

install() {
%{make_install}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/__pycache__
touch %{buildroot}%{_datadir}/%{name}/__pycache__/%{name}

for file in $(find %{buildroot}/usr/bin/lxc-* -type f -exec file {} ';' | grep "\<ELF\>" | grep -vE "*\.static" | awk -F ':' '{print $1}')
do
chrpath -d ${file}
done

for file in $(find %{buildroot}/usr/sbin/* -type f -exec file {} ';' | grep "\<ELF\>" | grep -vE "*\.static" | awk -F ':' '{print $1}')
do
chrpath -d ${file}
done

for file in $(find %{buildroot}/usr/libexec/lxc/lxc-* -type f -exec file {} ';' | grep "\<ELF\>" | grep -vE "*\.static" | awk -F ':' '{print $1}')
do
chrpath -d ${file}
done

chrpath -d %{buildroot}/usr/lib64/liblxc.so
chmod +x %{buildroot}/usr/lib64/liblxc.so
mkdir -p %{buildroot}%{_pkgdocdir}/api
cp -a AUTHORS README %{buildroot}%{_pkgdocdir}
cp -a doc/api/html/* %{buildroot}%{_pkgdocdir}/api/

mkdir -p %{buildroot}%{_localstatedir}/cache/%{name}

if [ ! -d %{buildroot}%{_sysconfdir}/sysconfig ]
then
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/sysconfig/%{name}
fi

rm -rf %{buildroot}%{_libdir}/liblxc.la
rm -rf %{buildroot}%{_sbindir}/init.%{name}.static
rm -rf %{buildroot}%{_sysconfdir}/default/%{name}
}

check() {
make check

}

