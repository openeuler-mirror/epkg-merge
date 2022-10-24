#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

mkdir cracklib-dicts
for dict in %{SOURCE1}
do
cp -fv ${dict} cracklib-dicts/
done
chmod +x util/cracklib-format

}

build() {
%if %{with python3}
sed -i 's,util/cracklib-check <,util/cracklib-check $(DESTDIR)/$(DEFAULT_CRACKLIB_DICT) <,' Makefile.in
py3include=`python3-config --includes | awk -F' ' '{print $1;}'`
export PYTHON=%{__python3}
export CFLAGS="%{optflags} $py3include"
abiflags=`python3-config --abiflags`
py_version="%{python3_version}$abiflags"
%configure \
    am_cv_python_version="$py_version" \
    %%{env.configureFlags}
make -C po update-gmo
make
%endif

}

install() {
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%if %{with python3}
make install DESTDIR=$RPM_BUILD_ROOT 'pythondir=${pyexecdir}'
%endif

./util/cracklib-format cracklib-dicts/* | \
./util/cracklib-packer $RPM_BUILD_ROOT/%{dictpath}
./util/cracklib-format $RPM_BUILD_ROOT/%{dictdir}/cracklib-small | \
./util/cracklib-packer $RPM_BUILD_ROOT/%{dictdir}/cracklib-small
rm -f $RPM_BUILD_ROOT/%{dictdir}/cracklib-small
sed s,/usr/lib/cracklib_dict,%{dictpath},g lib/crack.h > $RPM_BUILD_ROOT/%{_includedir}/crack.h
ln -s cracklib-format $RPM_BUILD_ROOT/%{_sbindir}/mkdict
ln -s cracklib-packer $RPM_BUILD_ROOT/%{_sbindir}/packer
touch $RPM_BUILD_ROOT/top

toprelpath=..
touch $RPM_BUILD_ROOT/top
while ! test -f $RPM_BUILD_ROOT/%{_libdir}/$toprelpath/top ; do
toprelpath=../$toprelpath
done
rm -f $RPM_BUILD_ROOT/top
if test %{dictpath} != %{_libdir}/cracklib_dict ; then
ln -s $toprelpath%{dictpath}.hwm $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.hwm
ln -s $toprelpath%{dictpath}.pwd $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.pwd
ln -s $toprelpath%{dictpath}.pwi $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.pwi
fi
rm -f $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/_cracklib*.*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/libcrack.la

%find_lang %{name}

}

check() {
make test

%ldconfig_scriptlets

}

