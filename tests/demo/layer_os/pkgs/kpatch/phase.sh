#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1 -Sgit

}

build() {
export CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"
%make_build

}

install() {
%make_install PREFIX=%{_prefix}

install -Dm 0500 -t %{buildroot}/%{_bindir} %{SOURCE1} %{SOURCE2}
mkdir -p %{buildroot}/opt/patch_workspace
install -Dm 0500 -t %{buildroot}/opt/patch_workspace/ %{SOURCE3}
pushd %{buildroot}/opt/patch_workspace
mkdir hotpatch package
popd

}

