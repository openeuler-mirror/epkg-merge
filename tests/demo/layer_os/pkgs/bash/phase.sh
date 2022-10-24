#!/usr/bash

prep() {
%autosetup -n %{name}-%{version} -p1

}

build() {
autoconf
%configure %%{env.configureFlags}
MFLAGS="CPPFLAGS=-D_GNU_SOURCE -DRECYCLES_PIDS -DDEFAULT_PATH_VALUE='\"/usr/local/bin:/usr/bin\"' `getconf LFS_CFLAGS`"
make "$MFLAGS" version.h
make "$MFLAGS" -C builtins
%make_build "$MFLAGS"

}

install() {
%make_install install-headers
ln -sf bash %{buildroot}%{_bindir}/sh
install -pDm 644 %SOURCE1 %{buildroot}/etc/skel/.bashrc
install -pDm 644 %SOURCE2 %{buildroot}/etc/skel/.bash_profile
install -pDm 644 %SOURCE3 %{buildroot}/etc/skel/.bash_logout
install -pDm 644 ./configs/alias.sh %{buildroot}%{_sysconfdir}/profile.d/alias.sh

for ea in alias bg cd command fc fg getopts hash jobs read type ulimit umask unalias wait
do
cat <<EOF > "%{buildroot}"/%{_bindir}/"$ea"
builtin $ea "\$@"
EOF
chmod +x "%{buildroot}"/%{_bindir}/"$ea"
done

%find_lang %{name}

}

check() {
make check

}

