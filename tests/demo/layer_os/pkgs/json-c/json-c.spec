%{!?_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global so_ver      5
%global reldate     20200726


Name:           json-c
Version:        0.15
Release:        5
Summary:        JSON implementation in C

License:        MIT
URL:            https://github.com/%{name}/%{name}
Source0:        %{url}/archive/%{name}-%{version}-%{reldate}.tar.gz

BuildRequires:  cmake gcc ninja-build

%description
JSON-C implements a reference counting object model that allows you
to easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C representation
of JSON objects.  It aims to conform to RFC 7159.


%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} == %{version}-%{release}

Patch6001:      backport-json-escape-str-avoid-harmless-unsigned-integer-overflow.patch

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%package        help
Summary:        Reference manual for json-c

BuildArch:      noarch

BuildRequires:  doxygen hardlink
Provides:       %{name}-doc = %{version}-%{release} 
Obsoletes:      %{name}-doc = %{version}-%{release}

%description    help
This package contains the reference manual for %{name}.

%prep
%autosetup -n %{name}-%{name}-%{version}-%{reldate} -p 1
 
# Remove pre-built html documentation.
rm -fr doc/html
 
# Update Doxyfile.
doxygen -s -u doc/Doxyfile.in
 
 
%build
%cmake \
  -DBUILD_STATIC_LIBS:BOOL=OFF       \
  -DCMAKE_BUILD_TYPE:STRING=RELEASE  \
  -DCMAKE_C_FLAGS_RELEASE:STRING=""  \
  -DDISABLE_BSYMBOLIC:BOOL=OFF       \
  -DDISABLE_WERROR:BOOL=ON           \
  -DENABLE_RDRAND:BOOL=ON            \
  -DENABLE_THREADING:BOOL=ON         \
  -G Ninja\
  %{!?__cmake_in_source_build:-S "%{_vpath_srcdir}"} \
  %{!?__cmake_in_source_build:-B "%{_vpath_builddir}"} \

%__cmake --build "%{_vpath_builddir}" %{?_smp_mflags} --verbose --target all doc
#%cmake_build

%check
%ninja_test -C %{_vpath_builddir} 

%install
#%cmake_install
DESTDIR="%{buildroot}" %__cmake --install "%{_vpath_builddir}"


mkdir -p %{buildroot}%{_pkgdocdir}
hardlink -cfv %{buildroot}%{_pkgdocdir}

%pretrans devel -p <lua>
path = "%{_includedir}/%{name}"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%ldconfig_scriptlets

%files
%license AUTHORS COPYING
%{_libdir}/lib%{name}.so.%{so_ver}*

%files devel
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files help
%doc %{_pkgdocdir}

%changelog
* Tue May 24 2022 fengtao <fengtao40@huawei.com> - 0.15-5
- we got upgrade error when upgrade json-c from very low version,
  for example json-c-0.11-5. because old version has a softlink:
  /usr/include/json-c  --> /usr/include/json
  and now, softlink has been removed. so, we fix this in pretrans

* Fri May 6 2022 wuchaochao <cyanrose@yeah.net> - 0.15-4
- add   backport-json-escape-str-avoid-harmless-unsigned-integer-overflow.patch

* Thu Apr 7 2022 wuchaochao <cyanrose@yeah.net> - 0.15-3
- add check

* Fri Mar 25 2022 wuchaochao <cyanrose@yeah.net> - 0.15-2
- move json-c

* Tue Sep 14 2021 hanhui <hanhui15@huawei.com> - 0.15-1
- update to 0.15

* Thu Sep 9 2021 liuyumeng <liuyumeng5@huawei.com> - 0.13.1-9
- fix broken RDRAND causes infinite looping

* Tue Jul 21 2020 wangye <wangye70@huawei.com> - 0.13.1-8
- fix hardlink path

* Fri May 22 2020 ruanweidong <ruanweidong1@huawei.com> -0.13.1-7
- fix CVE-2020-12762

* Sat Mar 21 2020 songnannan <songnannan2@huawei.com> - 0.13.1-6
- delete the check

* Tue Mar 3 2020 songnannan<songnannan2@huawei.com> - 0.13.1-5
- bugfix in oss-fuzz

* Thu Sep 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.13.1-4
- Package init
