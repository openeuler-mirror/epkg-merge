%bcond_without check

Name:           libarchive
Version:        3.6.1
Release:        1
Summary:        Multi-format archive and compression library
License:        BSD
URL:            https://www.libarchive.org/
Source0:        https://libarchive.org/downloads/%{name}-%{version}.tar.gz

BuildRequires:  gcc bison sharutils zlib-devel bzip2-devel xz-devel
BuildRequires:  lzo-devel e2fsprogs-devel libacl-devel libattr-devel
BuildRequires:  openssl-devel libxml2-devel lz4-devel automake libzstd-devel
BuildRequires:  autoconf libtool make

Patch0001:      0001-Drop-rmd160-from-OpenSSL.patch
Patch9000:	libarchive-uninitialized-value.patch

%description
%{name} is an open-source BSD-licensed C programming library that 
provides streaming access to a variety of different archive formats,
including tar, cpio, pax, zip, and ISO9660 images. The distribution 
also includes bsdtar and bsdcpio, full-featured implementations of 
tar and cpio that use %{name}.

%package 	devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description 	devel
%{name}-devel contains the header files for developing
applications that want to make use of %{name}.

%package_help

%package -n bsdtar
Summary:        Manipulate tape archives
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description -n bsdtar
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.
 
 
%package -n bsdcpio
Summary:        Copy files to and from archives
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description -n bsdcpio
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.
 
 
%package -n bsdcat
Summary:        Expand files to standard output
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description -n bsdcat
The bsdcat program typically takes a filename as an argument or reads standard
input when used in a pipe.  In both cases decompressed data it written to
standard output.

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf -ifv
%configure --disable-rpath --disable-static LT_SYS_LIBRARY_PATH=%_libdir
%disable_rpath

%make_build

%install
%make_install
%delete_la

replace ()
{
    filename=$1
    file=`basename "$filename"`
    binary=${file%%.*}
    pattern=${binary##bsd}

    awk "
        # replace the topic
        /^.Dt ${pattern^^} 1/ {
            print \".Dt ${binary^^} 1\";
            next;
        }
        # replace the first occurence of \"$pattern\" by \"$binary\"
        !stop && /^.Nm $pattern/ {
            print \".Nm $binary\" ;
            stop = 1 ;
            next;
        }
        # print remaining lines
        1;
    " "$filename" > "$filename.new"
    mv "$filename".new "$filename"
}

for manpage in bsdtar.1 bsdcpio.1
do
    installed_manpage=`find "$RPM_BUILD_ROOT" -name "$manpage"`
    replace "$installed_manpage"
done

%check
%if %{with check}
logfiles ()
{
    find -name '*_test.log' -or -name test-suite.log
}

tempdirs ()
{
    cat `logfiles` \
        | awk "match(\$0, /[^[:space:]]*`date -I`[^[:space:]]*/) { print substr(\$0, RSTART, RLENGTH); }" \
        | sort | uniq
}

cat_logs ()
{
    for i in `logfiles`
    do
        echo "=== $i ==="
        cat "$i"
    done
}

run_testsuite ()
{
    rc=0
    %make_build check -j1 || {
        # error happened - try to extract in koji as much info as possible
        cat_logs

        for i in `tempdirs`; do
            if test -d "$i" ; then
                find $i -printf "%p\n    ~> a: %a\n    ~> c: %c\n    ~> t: %t\n    ~> %s B\n"
                cat $i/*.log
            fi
        done
        return 1
    }
    cat_logs
}

run_testsuite

%endif

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/%{name}.so.13*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files help
%defattr(-,root,root)
%doc NEWS README.md
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*

%files -n bsdtar
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdtar
 
%files -n bsdcpio
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdcpio
 
%files -n bsdcat
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdcat

%changelog
* Mon Jun 6 2022 lin zhang <lin.zhang@turbolinux.com.cn> - 3.6.1-1
- Upgrade to 3.6.1

* Sat Apr 09 2022 wangkerong <wangkerong@h-paetners.com> - 3.5.2-3
- fix CVE-2021-36976,CVE-2021-31566,fix fuzz test

* Sat Mar 26 2022 wangkerong <wangkerong@h-paetners.com> - 3.5.2-2
- Eanable make check

* Fri Nov 26 2021 xingxing <xingxing@huawei.com> - 3.5.2-1
- Upgrade to version 3.5.2

* Thu Oct 14 2021 yangcheng <yagcheng87@huawei.com> - 3.5.1-2
- Type:CVE
- ID:CVE-2021-36976
- SUG:NA
- DESC:fix CVE-2021-36976

* Fri Jan 29 2021 zhanzhimin <zhanzhimin@huawei.com> - 3.5.1-1
- Upgrade to version 3.5.1

* Fri Aug 21 2020 yanan <yanan@huawei.com> - 3.4.3-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Avoid stack overflow in read_data_compressed

* Tue Jul 28 2020 zhangnaru <zhangnaru@huawei.com> - 3.4.3-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Upgrade to version 3.4.3

* Mon Apr 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.4.1-3
- Type:cves
- ID:CVE-2020-9308
- SUG:NA
- DESC:fix CVE-2020-9308

* Tue Mar 10 2020 songnannan <songnannan2@huawei.com> - 3.4.1-2
- bugfix about uninitialized value

* Wed Jan 8 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.4.1-1
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: update to 3.4.1

* Fri Jan 3 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.4.0-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:bugfix about CVE-2019-19221.patch

* Wed Oct 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.4.0-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:delete the comment for patch0

* Mon Sep 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.4.0-1
- Package init
