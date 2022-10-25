#!/usr/bash

prep() {
%autosetup -n %{name}-%{name}-%{version}-%{reldate} -p 1

rm -fr doc/html

doxygen -s -u doc/Doxyfile.in


}

build() {
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

}

check() {
%ninja_test -C %{_vpath_builddir}

}

install() {
DESTDIR="%{buildroot}" %__cmake --install "%{_vpath_builddir}"


mkdir -p %{buildroot}%{_pkgdocdir}
hardlink -cfv %{buildroot}%{_pkgdocdir}

}

