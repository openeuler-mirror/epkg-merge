#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
%configure
%make_build

}

install() {
%make_install
%delete_la_and_a
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*

%find_lang %{name}

}

check() {
if test 0 = "$(id -u)"; then
sed -e 's|test/root/permissions.test||' -i test/Makemodule.am Makefile.in Makefile
fi
if ! runuser -u bin -- "${PWD}/setfacl" --version; then
sed -e 's|test/root/setfacl.test||' -i test/Makemodule.am Makefile.in Makefile
fi

%make_build check

}

