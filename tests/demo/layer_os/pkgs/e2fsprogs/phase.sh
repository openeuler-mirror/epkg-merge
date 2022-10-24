#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1


}

build() {
%configure CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %%{env.configureFlags}
%make_build V=1

}

install() {
make install install-libs DESTDIR=%{buildroot} INSTALL="%{__install} -p" \
    root_sbindir=%{_sbindir} root_libdir=%{_libdir}
chmod +w %{buildroot}%{_libdir}/*.a

%define multilib_arches %{ix86} x86_64

%ifarch %{multilib_arches}
mv -f %{buildroot}%{_includedir}/ext2fs/ext2_types.h \
      %{buildroot}%{_includedir}/ext2fs/ext2_types-%{_arch}.h

install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/ext2fs/ext2_types.h

%endif

%find_lang %{name}

rm -f %{buildroot}/etc/cron.d/e2scrub_all
rm -f %{buildroot}%{_libdir}/e2fsprogs/e2scrub_all_cron

%ifarch i686
rm -rf %{buildroot}%{_unitdir}/e2scrub*
%endif

}

check() {
make fullcheck

%ldconfig_scriptlets

}

