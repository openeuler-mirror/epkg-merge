#!/usr/bash

prep() {
%autosetup -n glib-%{version} -p1

}

build() {
rm -rf glib/pcre/*.[ch]

%meson --default-library=both  -Ddtrace=true  \
%ifnarch i686
%if %{?openEuler:1}0
-Dsysprof=enabled \
%endif
-Dman=true -Dgtk_doc=true \
%else
-Dsysprof=disabled -Dman=false -Dgtk_doc=false \
%endif
-Dsystemtap=true -Dinstalled_tests=true \
    -Dglib_debug=disabled

%meson_build
find . -name *.dtrace-temp.c -exec rm -f {} \;

}

check() {
%meson_test

}

install() {
%meson_install
%global py_reproducible_pyc_path %{buildroot}%{_datadir}
touch -r gio/gdbus-2.0/codegen/config.py.in %{buildroot}%{_datadir}/glib-2.0/codegen/*.py
chrpath --delete %{buildroot}%{_libdir}/*.so

export PYTHONHASHSEED=0
%py_byte_compile %{__python3} %{buildroot}%{_datadir}

mv %{buildroot}%{_bindir}/gio-querymodules %{buildroot}%{_bindir}/gio-querymodules-%{__isa_bits}
sed -i -e "/^gio_querymodules=/s/gio-querymodules/gio-querymodules-%{__isa_bits}/" %{buildroot}%{_libdir}/pkgconfig/gio-2.0.pc
mkdir -p %{buildroot}%{_libdir}/gio/modules
touch %{buildroot}%{_libdir}/gio/modules/giomodule.cache

rm -rf %{buildroot}/%{_datadir}/gdb/auto-load/%{_libdir}/__pycache__
rm -rf %{buildroot}/%{_datadir}/glib-2.0/codegen/__pycache__
rm -rf %{buildroot}/%{_datadir}/glib-2.0/gdb/__pycache__

chrpath -d %{buildroot}%{_libexecdir}/installed-tests/glib/gdbus-peer

%find_lang glib20

%transfiletriggerin -- %{_libdir}/gio/modules
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%transfiletriggerpostun -- %{_libdir}/gio/modules
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%transfiletriggerin -- %{_datadir}/glib-2.0/schemas
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%transfiletriggerpostun -- %{_datadir}/glib-2.0/schemas
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

}

