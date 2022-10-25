#!/usr/bash

post:binutils-help() {
for info in as.info.gz binutils.info.gz gprof.info.gz ld.info.gz
do
/sbin/install-info --info-dir=%{_infodir} %{_infodir}/$info
done
}

preun:binutils-help() {
if [ $1 = 0 ]; then
if [ -e %{_infodir}/binutils.info.gz ]
then
for info in as.info.gz binutils.info.gz gprof.info.gz ld.info.gz
do
/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/$info
done
fi
fi
}

postun:binutils-help() {
if [ -e %{_infodir}/binutils.info.gz ]
then
for info in as.info.gz binutils.info.gz gprof.info.gz ld.info.gz
do
/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/$info
done
fi
}

post() {
%__rm -f %{_bindir}/ld
%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/ld.bfd %{ld_bfd_priority}

%if %{with gold}
%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/ld.gold %{ld_gold_priority}
%endif

if [ $1 = 0 ]; then
%{_sbindir}/alternatives --auto ld
fi

/sbin/ldconfig

}

preun() {
if [ $1 = 0 ]; then
%{_sbindir}/alternatives --remove ld %{_bindir}/ld.bfd

%if %{with gold}
%{_sbindir}/alternatives --remove ld %{_bindir}/ld.gold
%endif
fi

}

postun() {
/sbin/ldconfig

}

