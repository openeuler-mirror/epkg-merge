#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

for f in ANNOUNCE; do
iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
touch -r ${f}{,_} && mv -f ${f}{_,}
done

}

build() {
abi5_options="--with-chtype=long"

for abi in 5 6; do
for char in narrowc widec; do
mkdir $char$abi
pushd $char$abi
ln -s ../configure .

[ $abi = 6 -a $char = widec ] && progs=yes || progs=no

%configure %%{env.configureFlags} $(
echo --with-abi-version=$abi
[ $abi = 5 ] && echo $abi5_options
[ $char = widec ] && echo --enable-widec
[ $progs = yes ] || echo --without-progs
)

make %{?_smp_mflags} libs
[ $progs = yes ] && make %{?_smp_mflags} -C progs

popd
done
done

}

install() {
make -C narrowc5 DESTDIR=$RPM_BUILD_ROOT install.libs
rm ${RPM_BUILD_ROOT}%{_libdir}/lib{tic,tinfo}.so.5*
make -C widec5 DESTDIR=$RPM_BUILD_ROOT install.libs
make -C narrowc6 DESTDIR=$RPM_BUILD_ROOT install.libs
rm ${RPM_BUILD_ROOT}%{_libdir}/lib{tic,tinfo}.so.6*
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.{libs,progs,data,includes,man}

chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/terminfo

baseterms=

for termname in \
    ansi dumb linux vt100 vt100-nav vt102 vt220 vt52 \
    Eterm\* aterm bterm cons25 cygwin eterm\* gnome gnome-256color hurd jfbterm \
    konsole konsole-256color mach\* mlterm mrxvt nsterm putty{,-256color} pcansi \
    rxvt{,-\*} screen{,-\*color,.[^mlp]\*,.linux,.mlterm\*,.putty{,-256color},.mrxvt} \
    st{,-\*color} sun teraterm teraterm2.3 tmux{,-\*} vte vte-256color vwmterm \
    wsvt25\* xfce xterm xterm-\*
do
for i in $RPM_BUILD_ROOT%{_datadir}/terminfo/?/$termname; do
for t in $(find $RPM_BUILD_ROOT%{_datadir}/terminfo -samefile $i); do
baseterms="$baseterms $(basename $t)"
done
done
done 2> /dev/null
for t in $baseterms; do
echo "%dir %{_datadir}/terminfo/${t::1}"
echo %{_datadir}/terminfo/${t::1}/$t
done 2> /dev/null | sort -u > terms.base
find $RPM_BUILD_ROOT%{_datadir}/terminfo \! -type d | \
    sed "s|^$RPM_BUILD_ROOT||" | while read t
do
echo "%dir $(dirname $t)"
echo $t
done 2> /dev/null | sort -u | comm -2 -3 - terms.base > terms.term

mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncurses
ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

for l in $RPM_BUILD_ROOT%{_libdir}/libncurses{,w}.so; do
soname=$(basename $(readlink $l))
rm -f $l
echo "INPUT($soname -ltinfo)" > $l
done

rm -f $RPM_BUILD_ROOT%{_libdir}/libcurses{,w}.so
echo "INPUT(-lncurses)" > $RPM_BUILD_ROOT%{_libdir}/libcurses.so
echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so

echo "INPUT(-ltinfo)" > $RPM_BUILD_ROOT%{_libdir}/libtermcap.so

rm -f $RPM_BUILD_ROOT%{_bindir}/ncurses*5-config
rm -f $RPM_BUILD_ROOT%{_libdir}/terminfo
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*_g.pc

xz NEWS

%ldconfig_scriptlets
%ldconfig_scriptlets libs
%ldconfig_scriptlets compat-libs

}

