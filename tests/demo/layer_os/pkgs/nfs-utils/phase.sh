#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1
find -name \*.py -exec sed -r -i '1s|^#!\s*/usr/bin.*python.*|#!%{__python3}|' {} \;

}

build() {
sh -x autogen.sh
%configure \
    CFLAGS="%{build_cflags} -D_FILE_OFFSET_BITS=64" \
    LDFLAGS="%{build_ldflags}" \
    %%{env.configureFlags}

%make_build all

}

install() {
%make_install


install -D -m 644 utils/nfsidmap/id_resolver.conf $RPM_BUILD_ROOT%{_sysconfdir}/request-key.d/id_resolver.conf
install -s -m 755 tools/rpcdebug/rpcdebug $RPM_BUILD_ROOT%{_sbindir}
install -m 644 utils/mount/nfsmount.conf  $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 nfs.conf  $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 support/nfsidmap/idmapd.conf $RPM_BUILD_ROOT%{_sysconfdir}

touch $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/rmtab
mv $RPM_BUILD_ROOT%{_sbindir}/rpc.statd $RPM_BUILD_ROOT/sbin

mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/rpc_pipefs
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/nfs/v4recovery
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/exports.d

cd $RPM_BUILD_ROOT%{_unitdir}
ln -s rpc-statd.service nfs-lock.service
ln -s rpc-gssd.service nfs-secure.service
ln -s nfs-server.service nfs.service
ln -s nfs-idmapd.service  nfs-idmap.service

rm -rf $RPM_BUILD_ROOT%{_libdir}/{*.a,*.la}
rm -rf $RPM_BUILD_ROOT%{_libdir}/libnfsidmap/{*.a,*.la}

}

check() {
make check

}

