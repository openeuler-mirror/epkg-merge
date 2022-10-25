%bcond_without python3

%define dictdir %{_datadir}/cracklib
%define dictpath %{dictdir}/pw_dict

Name: cracklib
Version: 2.9.7
Release: 8
Summary: A password-checking library

License: LGPLv2+
URL: http://sourceforge.net/projects/cracklib/
Source0: https://github.com/cracklib/cracklib/releases/download/v%{version}/cracklib-%{version}.tar.gz
Source1: https://github.com/cracklib/cracklib/releases/download/v%{version}/cracklib-words-%{version}.gz
Patch0: fix-problem-of-error-message-about-simplistic-passwo.patch
Patch1: backport-cracklib-2.9.6-lookup.patch
# After fix-problem-of-error-message-about-simplistic-passwo.patch
Patch2: fix-error-length-about-simplistic-password.patch
Patch3: fix-truncating-dict-file-without-input-data.patch

BuildRequires: gcc, words, gettext, gettext-autopoint, zlib-devel
%if %{with python3}
BuildRequires: python3-devel
%endif
Conflicts: cracklib-dicts < 2.8
Requires: gzip

Provides: cracklib-dicts
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: cracklib-dicts
Obsoletes: %{name}-python < %{version}-%{release}

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics, with the purpose of preventing users
from choosing passwords that could easily be guessed.

CrackLib is a library containing a C function which may be used in a
"passwd"-like program. If you install CrackLib, you will also want to
install the cracklib-dicts package.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The cracklib-devel package contains the header files and libraries needed
for compiling applications which use cracklib.

%package_help

%if %{with python3}
%package -n python3-cracklib
Summary: Python 3 bindings for applications which use cracklib
Requires: %{name} = %{version}-%{release}

%description -n python3-cracklib
The python3-cracklib package contains a module which permits applications
written in the Python 3 programming language to use cracklib.
%endif

%prep
%autosetup -n %{name}-%{version} -p1

mkdir cracklib-dicts
for dict in %{SOURCE1}
do
        cp -fv ${dict} cracklib-dicts/
done
chmod +x util/cracklib-format

%build
%if %{with python3}
sed -i 's,util/cracklib-check <,util/cracklib-check $(DESTDIR)/$(DEFAULT_CRACKLIB_DICT) <,' Makefile.in
py3include=`python3-config --includes | awk -F' ' '{print $1;}'`
export PYTHON=%{__python3}
export CFLAGS="%{optflags} $py3include"
abiflags=`python3-config --abiflags`
py_version="%{python3_version}$abiflags"
%configure \
    am_cv_python_version="$py_version" \
    --disable-static \
    --with-pic \
    --with-python \
    --with-default-dict=%{dictpath}
make -C po update-gmo
make
%endif

%install
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

%check
make test

%ldconfig_scriptlets

%files -f %{name}.lang
%defattr(-,root,root)
%doc README-LICENSE AUTHORS
%license COPYING.LIB
%{_sbindir}/*cracklib*
%{_sbindir}/mkdict
%{_sbindir}/packer
%{_libdir}/libcrack.so.*
%{_libdir}/cracklib_dict.*
%dir %{_datadir}/cracklib
%config(noreplace) %{_datadir}/cracklib/pw_dict.*
%{_datadir}/cracklib/cracklib-small.*
%{_datadir}/cracklib/cracklib.magic

%files devel
%{_includedir}/*
%{_libdir}/libcrack.so

%files help
%doc README README-WORDS NEWS

%if %{with python3}
%files -n python3-cracklib
%{_libdir}/python3*/site-packages/_cracklib*.so
%{_libdir}/python3*/site-packages/*.py*
%{_libdir}/python3*/site-packages/__pycache__/*
%endif

%changelog
* Sat Aug 13 2022 yixiangzhike <yixiangzhike007@163.com> - 2.9.7-8
- fix issue of truncating dict file without input data
- fix error length about simplistic password

* Mon Dec 6 2021 yixiangzhike <yixiangzhike007@163.com> - 2.9.7-7
- fix lookup for word in FindPW()

* Mon May 24 2021 yixiangzhike <zhangxingliang3@huawei.com> - 2.9.7-6
- add %%config(noreplace) for pw_dict

* Thu Oct 22 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.9.7-5
- remove python2

* Mon Sep 14 2020 wangchen <wangchen137@huawei.com> - 2.9.7-4
- Modify the URL of Source

* Thu Sep 3 2020 zhangxingliang <zhangxingliang3@huawei.com> - 2.9.7-3
- Add python3-cracklib package

* Sat Jan 18 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.9.7-2
- fix problem of error message about simplistic password

* Fri Jan 10 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.9.7-1
- clean code

* Fri Sep 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.6-17
- Add python2-cracklib package

* Fri Sep 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.6-16
- Package init
