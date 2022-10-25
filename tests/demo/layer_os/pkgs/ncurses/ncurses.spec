Name:          ncurses
Version:       6.3
Release:       4
Summary:       Terminal control library
License:       MIT
URL:           https://invisible-island.net/ncurses/ncurses.html
Source0:       https://invisible-mirror.net/archives/ncurses/ncurses-%{version}.tar.gz

Patch8:        ncurses-config.patch
Patch9:        ncurses-libs.patch
Patch11:       ncurses-urxvt.patch
Patch12:       ncurses-kbs.patch
Patch13:       backport-CVE-2022-29458.patch

BuildRequires: gcc gcc-c++ gpm-devel pkgconfig

Requires:      %{name}-base = %{version}-%{release}
Requires:      %{name}-libs = %{version}-%{release}

Obsoletes:     rxvt-unicode-terminfo < 9.22-18
Provides:      %{name}-c++-libs = %{version}-%{release}
Obsoletes:     %{name}-c++-libs < %{version}-%{release}
Provides:      %{name}-term = %{version}-%{release}
Obsoletes:     %{name}-term < %{version}-%{release}

%description
The ncurses (new curses) library is a free software emulation of 
curses in System V Release 4.0 (SVr4), and more. It uses terminfo 
format, supports pads and color and multiple highlights and forms 
characters and function-key mapping, and has all the other SVr4-curses 
enhancements over BSD curses. SVr4 curses became the basis of X/Open Curses.

%package       base
Summary:       Descriptions of common terminals
BuildArch:     noarch

%description   base
This package contains descriptions of common terminals.

%package       libs
Summary:       Libraries for %{name}
Requires:      %{name}-base = %{version}-%{release}

%description   libs
Libraries for %{name}.

%package       devel
Summary:       Development files for the ncurses library
Requires:      %{name}-libs = %{version}-%{release}
Requires:      %{name}-c++-libs = %{version}-%{release}
Requires:      pkgconfig
Provides:      %{name}-static = %{version}-%{release}
Obsoletes:     %{name}-static < %{version}-%{release}
Provides:      libtermcap-devel = 2.0.8-48
Obsoletes:     libtermcap-devel < 2.0.8-48


%description   devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.a, including static libraries 
of the ncurses library.

%package compat-libs
Summary: Ncurses compatibility libraries
Group: System Environment/Libraries
Requires: %{name}-base = %{version}-%{release}

%description compat-libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ABI version 5 of the ncurses libraries for
compatibility.

%package       help
Summary: Ncurse help document
Requires: %{name} = %{version}-%{release}

%description   help
This package contains development documentation, manuals 
for interface function, and related documents.

%prep
%autosetup -n %{name}-%{version} -p1

for f in ANNOUNCE; do
    iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
        touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
common_options="--enable-colorfgbg --enable-hard-tabs --enable-overwrite \
    --enable-pc-files --enable-xmc-glitch --disable-wattr-macros \
    --with-cxx-shared --with-ospeed=unsigned \
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \
    --with-shared \
    --with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo \
    --with-termlib=tinfo --with-ticlib=tic --with-xterm-kbs=DEL \
    --without-ada"
abi5_options="--with-chtype=long"

for abi in 5 6; do
    for char in narrowc widec; do
        mkdir $char$abi
        pushd $char$abi
        ln -s ../configure .

        [ $abi = 6 -a $char = widec ] && progs=yes || progs=no

        %configure $(
            echo $common_options --with-abi-version=$abi
            [ $abi = 5 ] && echo $abi5_options
            [ $char = widec ] && echo --enable-widec
            [ $progs = yes ] || echo --without-progs
        )

        make %{?_smp_mflags} libs
        [ $progs = yes ] && make %{?_smp_mflags} -C progs

        popd
    done
done

%install
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

# prepare -base and -term file lists
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

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncurses
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

# don't require -ltinfo when linking with --no-add-needed
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

%files -f terms.term
%doc ANNOUNCE AUTHORS
%doc c++/README*
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/[cirt]*
%{_libdir}/libncurses++*.so.6*

%files base -f terms.base
%dir %{_sysconfdir}/terminfo
%{_datadir}/tabset
%dir %{_datadir}/terminfo

%files libs
%{_libdir}/lib*.so.6*
%exclude %{_libdir}/libncurses++*.so.6*

%files devel
%{_bindir}/ncurses*-config
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/ncurses/*.h
%{_includedir}/ncursesw/*.h
%{_includedir}/*.h

%files compat-libs
%{_libdir}/lib*.so.5*

%files help
%doc NEWS.xz README TO-DO
%doc doc/html/hackguide.html
%doc doc/html/ncurses-intro.html
%doc misc/ncurses.supp
%{_mandir}/man1/ncurses*-config*
%{_mandir}/man3/*
%{_mandir}/man1/[cirt]*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
* Thu Jun 16 2022 yanglu <yanglu72@h-partners.com> - 6.3-4
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:delete marcos in changelog

* Thu Apr 28 2022 gaihuiying <eaglegai@163.com> - 6.3-3
- Type:CVE
- CVE:CVE-2022-29458
- SUG:NA
- DESC:fix CVE-2022-29458

* Sat Apr 16 2022 xingwei<xingwei14@h-partners.com> - 6.3-2
- Type:requirements
- CVE:NA
- SUG:NA
- DESC:split compat-libs from ncurses

* Mon Mar 21 2022 xihaochen<xihaochen@h-partners.com> - 6.3-1
- Type:bugfix
- CVE:NA
- SUG:NA
- DESC:update to 6.3

* Tue Oct 12 2021 xihaochen<xihaochen@huawei.com> - 6.2-2
- Type:CVE
- CVE:CVE-2021-39537
- SUG:NA
- DESC:fix CVE-2021-39537

* Thu Apr 16 2020 huzunhao <huzunhao2@huawei.com> - 6.2-1
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:update to 6.2

* Mon Feb 17 2020 hexiujun <hexiujun1@huawei.com> - 6.1-14
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:unpack libs subpackage

* Fri Jan 10 2020 openEuler Buildteam <buildteam@openeuler.org> - 6.1-13
- update to 20191102

* Sat Dec 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.1-12
- Type:cves
- ID:CVE-2019-17594  CVE-2019-17595
- SUG:NA
- DESC:fix CVE-2019-17594 and CVE-2019-17595

* Wed Oct 30 2019 shenyangyang <shenyangyang4@huawei.com> - 6.1-11
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify the obsoletes version

* Thu Oct 17 2019 caomeng <caomeng5@huawei.com> - 6.1-10
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add ncurses-compat-libs

* Wed Sep 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 6.1-9
- Package init
