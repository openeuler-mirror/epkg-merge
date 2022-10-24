#!/usr/bash

prep() {
%autosetup -n shadow-%{version} -p1

iconv -f ISO88591 -t utf-8  doc/HOWTO > doc/HOWTO.utf8
cp -f doc/HOWTO.utf8 doc/HOWTO

cp -a %{SOURCE3} %{SOURCE4} .

}

build() {
export CFLAGS="$RPM_OPT_FLAGS -fpie"
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"

autoreconf -fiv
%configure %%{env.configureFlags}
%make_build

}

install() {
rm -rf $RPM_BUILD_ROOT
%make_install gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale MKINSTALLDIRS=`pwd`/mkinstalldirs
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}/default
install -p -c -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/login.defs
install -p -c -m 0600 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/default/useradd
install -p -c -m 0644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/chpasswd
install -p -c -m 0644 %{SOURCE6} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/newusers

ln -s useradd $RPM_BUILD_ROOT%{_sbindir}/adduser
ln -s useradd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/adduser.8
for subdir in $RPM_BUILD_ROOT/%{_mandir}/{??,??_??,??_??.*}/man* ; do
test -d $subdir && test -e $subdir/useradd.8 && echo ".so man8/useradd.8" > $subdir/adduser.8
done

rm $RPM_BUILD_ROOT/%{_bindir}/chfn
rm $RPM_BUILD_ROOT/%{_bindir}/chsh
rm $RPM_BUILD_ROOT/%{_bindir}/expiry
rm $RPM_BUILD_ROOT/%{_bindir}/groups
rm $RPM_BUILD_ROOT/%{_bindir}/login
rm $RPM_BUILD_ROOT/%{_bindir}/passwd
rm $RPM_BUILD_ROOT/%{_bindir}/su
rm $RPM_BUILD_ROOT/%{_bindir}/faillog
rm $RPM_BUILD_ROOT/%{_sbindir}/logoutd
rm $RPM_BUILD_ROOT/%{_sbindir}/nologin
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/man3/getspnam.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man3/getspnam.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/faillog.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/faillog.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/faillog.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/faillog.*
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/chfn
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/chsh
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/login
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/passwd
rm $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/su

find $RPM_BUILD_ROOT%{_mandir} -depth -type d -empty -delete
%find_lang shadow
for dir in $(ls -1d $RPM_BUILD_ROOT%{_mandir}/{??,??_??}) ; do
dir=$(echo $dir | sed -e "s|^$RPM_BUILD_ROOT||")
lang=$(basename $dir)
done

echo $(ls)
mkdir -p $RPM_BUILD_ROOT/%{includesubiddir}
install -m 644 libsubid/subid.h $RPM_BUILD_ROOT/%{includesubiddir}/

rm -f $RPM_BUILD_ROOT/%{_libdir}/libsubid.la

}

