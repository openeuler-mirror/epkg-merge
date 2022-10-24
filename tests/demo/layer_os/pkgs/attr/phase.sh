#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure %%{env.configureFlags}
make %{?_smp_mflags}

}

install() {
%make_install
chrpath -d $RPM_BUILD_ROOT%{_bindir}/attr
chrpath -d $RPM_BUILD_ROOT%{_bindir}/getfattr
chrpath -d $RPM_BUILD_ROOT%{_bindir}/setfattr


rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*

ln -fs ../sys/xattr.h $RPM_BUILD_ROOT%{_includedir}/attr/xattr.h

%find_lang %{name}

}

check() {
if ./setfattr -n user.name -v value .; then
make check || exit $?
else
echo '*** xattrs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi

}

