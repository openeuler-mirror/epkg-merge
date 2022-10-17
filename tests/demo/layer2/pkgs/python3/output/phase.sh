#!/usr/bash

prep() {
%setup -q -n Python-%{version}
find -name '*.exe' -print -delete
rm -r Modules/expat
rm Lib/ensurepip/_bundled/*.whl
rm configure pyconfig.h.in

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%patch8 -p1

}

build() {
autoconf
autoheader

topdir=$(pwd)

%if %{with optimizations}
%global optimizations_flag "--enable-optimizations"
%else
%global optimizations_flag "--disable-optimizations"
%endif

%global extension_cflags ""
%global extension_ldflags ""

export CFLAGS="%{extension_cflags} -D_GNU_SOURCE -fPIC -fwrapv -fstack-protector-strong -D_FORTIFY_SOURCE=2 -O2"
export CFLAGS_NODIST="%{build_cflags} -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="%{extension_cxxflags} -D_GNU_SOURCE -fPIC -fwrapv"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="%{extension_cflags} -D_GNU_SOURCE -fPIC -fwrapv"
export LINKCC="gcc"
export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
export LDFLAGS="%{extension_ldflags} -g $(pkg-config --libs-only-L openssl)"
export LDFLAGS_NODIST="%{build_ldflags} -g $(pkg-config --libs-only-L openssl)"

DebugBuildDir=build/debug
mkdir -p ${DebugBuildDir}
pushd ${DebugBuildDir}

%global _configure $topdir/configure

%configure \
  --with-platlibdir=%{_lib} \
  --without-static-libpython \
  --with-wheel-pkg-dir=%{_datadir}/python-wheels \
  --enable-ipv6 \
  --enable-shared \
  --with-computed-gotos=yes \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --with-dtrace \
  --with-ssl-default-suites=openssl \
%ifarch %{valgrind_arches}
--with-valgrind \
%endif
--without-ensurepip \
  --with-pydebug --enable-loadable-sqlite-extensions

%make_build EXTRA_CFLAGS="$CFLAGS -Og"

popd

OptimizedBuildDir=build/optimized
mkdir -p ${OptimizedBuildDir}
pushd ${OptimizedBuildDir}

%global _configure $topdir/configure

%configure \
  --with-platlibdir=%{_lib} \
  --without-static-libpython \
  --with-wheel-pkg-dir=%{_datadir}/python-wheels \
  --enable-ipv6 \
  --enable-shared \
  --with-computed-gotos=yes \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --with-dtrace \
  --with-ssl-default-suites=openssl \
%ifarch %{valgrind_arches}
--with-valgrind \
%endif
--without-ensurepip \
  %{optimizations_flag} --enable-loadable-sqlite-extensions

%make_build EXTRA_CFLAGS="$CFLAGS"

popd

}

install() {

topdir=$(pwd)

DirHoldingGdbPy=%{_prefix}/lib/debug/%{_libdir}
mkdir -p %{buildroot}$DirHoldingGdbPy

%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h
%global _pyconfig_h pyconfig-%{wordsize}.h

DebugBuildDir=build/debug
mkdir -p ${DebugBuildDir}
pushd ${DebugBuildDir}
make DESTDIR=%{buildroot} INSTALL="install -p" EXTRA_CFLAGS="-O0" install
popd

PathOfGdbPy=$DirHoldingGdbPy/%{py_INSTSONAME_debug}-%{version}-%{release}.%{_arch}.debug-gdb.py
cp Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy

mv %{buildroot}%{_bindir}/python%{LDVERSION_debug}-{,`uname -m`-}config
echo -e '#!/bin/sh\nexec `dirname $0`/python'%{LDVERSION_debug}'-`uname -m`-config "$@"' > \
  %{buildroot}%{_bindir}/python%{LDVERSION_debug}-config
echo '[ $? -eq 127 ] && echo "Could not find python'%{LDVERSION_debug}'-`uname -m`-config. Look around to see available arches." >&2' >> \
  %{buildroot}%{_bindir}/python%{LDVERSION_debug}-config
chmod +x %{buildroot}%{_bindir}/python%{LDVERSION_debug}-config

mv %{buildroot}%{_includedir}/python%{LDVERSION_debug}/pyconfig.h \
   %{buildroot}%{_includedir}/python%{LDVERSION_debug}/%{_pyconfig_h}
install -D -m 0644 %{SOURCE1} %{buildroot}%{_includedir}/python%{LDVERSION_debug}/pyconfig.h

OptimizedBuildDir=build/optimized
mkdir -p ${OptimizedBuildDir}
pushd ${OptimizedBuildDir}
make DESTDIR=%{buildroot} INSTALL="install -p" EXTRA_CFLAGS="" install
popd

PathOfGdbPy=$DirHoldingGdbPy/%{py_INSTSONAME_optimized}-%{version}-%{release}.%{_arch}.debug-gdb.py
cp Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy

mv %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-{,`uname -m`-}config
echo -e '#!/bin/sh\nexec `dirname $0`/python'%{LDVERSION_optimized}'-`uname -m`-config "$@"' > \
  %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config
echo '[ $? -eq 127 ] && echo "Could not find python'%{LDVERSION_optimized}'-`uname -m`-config. Look around to see available arches." >&2' >> \
  %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config
chmod +x %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config

mv %{buildroot}%{_includedir}/python%{LDVERSION_optimized}/pyconfig.h \
   %{buildroot}%{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}
install -D -m 0644 %{SOURCE1} %{buildroot}%{_includedir}/python%{LDVERSION_optimized}/pyconfig.h
install -d -m 0755 %{buildroot}%{pylibdir}/site-packages/__pycache__
install -d -m 0755 %{buildroot}%{_prefix}/lib/python%{branchversion}/site-packages/__pycache__

install -D -m 0644 Lib/idlelib/Icons/idle_16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/idle3.png
install -D -m 0644 Lib/idlelib/Icons/idle_32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/idle3.png
install -D -m 0644 Lib/idlelib/Icons/idle_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/idle3.png

sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/distutils/sysconfig.py \
  %{buildroot}%{pylibdir}/sysconfig.py

cp -p Tools/scripts/pathfix.py %{buildroot}%{_bindir}/

for tool in pygettext msgfmt; do
cp -p Tools/i18n/${tool}.py %{buildroot}%{_bindir}/${tool}%{branchversion}.py
ln -s ${tool}%{branchversion}.py %{buildroot}%{_bindir}/${tool}3.py
done

LD_LIBRARY_PATH=./build/optimized ./build/optimized/python \
  Tools/scripts/pathfix.py \
  -i "%{_bindir}/python%{branchversion}" -pn \
  %{buildroot} \
  %{buildroot}%{_bindir}/*%{branchversion}.py \
  %{?with_gdb_hooks:%{buildroot}$DirHoldingGdbPy/*.py}

rm -rf %{buildroot}%{pylibdir}/test/test_tools

find %{buildroot} -name \*.py \
  \( \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \; \
  -print -exec sed -i '1d' {} \; \) -o \( \
  -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \; \
  -exec chmod a-x {} \; \) \)

find %{buildroot} -name \*.bat -exec rm {} \;

find %{buildroot}/ -name "*~" -exec rm -f {} \;
find . -name "*~" -exec rm -f {} \;

rm %{buildroot}%{pylibdir}/LICENSE.txt

find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{branchversion} %{buildroot}%{_libdir}/python%{branchversion}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{branchversion} -O -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2], optimize=opt) for opt in range(3) for f in sys.argv[1:]]' || :

rm -rf %{buildroot}%{_bindir}/__pycache__

find %{buildroot} -perm 555 -exec chmod 755 {} \;

ln -s \
  %{_bindir}/python%{LDVERSION_debug} \
  %{buildroot}%{_bindir}/python3-debug

ln -s %{_bindir}/python3 %{buildroot}%{_bindir}/python

mv %{buildroot}%{_bindir}/2to3-%{branchversion} %{buildroot}%{_bindir}/2to3

}

check() {
topdir=$(pwd)

BEP_WHITELIST_TMP="$BEP_WHITELIST"
BEP_GTDLIST_TMP="$BEP_GTDLIST"
export BEP_WHITELIST="python python-debug "$BEP_WHITELIST""
export BEP_GTDLIST=`echo $BEP_GTDLIST | sed 's/ python / /g'`

export OPENSSL_CONF=/non-existing-file

LD_LIBRARY_PATH=$(pwd)/build/debug $(pwd)/build/debug/python -m test.pythoninfo

WITHIN_PYTHON_RPM_BUILD= \
LD_LIBRARY_PATH=$(pwd)/build/debug $(pwd)/build/debug/python -m test.regrtest \
    -wW --slowest -j0 --timeout 1800 \
    -x test_distutils \
    -x test_bdist_rpm \
    -x test_gdb \
    -x test_socket \
    -x test_asyncio

export OPENSSL_CONF=/non-existing-file
LD_LIBRARY_PATH=$(pwd)/build/optimized $(pwd)/build/optimized/python -m test.pythoninfo

WITHIN_PYTHON_RPM_BUILD= \
LD_LIBRARY_PATH=$(pwd)/build/optimized $(pwd)/build/optimized/python -m test.regrtest \
    -wW --slowest -j0 --timeout 1800 \
    -x test_distutils \
    -x test_bdist_rpm \
    -x test_gdb \
    -x test_socket \
    -x test_asyncio

export BEP_WHITELIST="$BEP_WHITELIST_TMP"
export BEP_GTDLIST="$BEP_GTDLIST_TMP"

}

