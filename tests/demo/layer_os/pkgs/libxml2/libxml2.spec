Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.9.14
Release: 2
License: MIT
Group: Development/Libraries
Source: https://download.gnome.org/sources/%{name}/2.9/%{name}-%{version}.tar.xz

Patch0: libxml2-multilib.patch
Patch1: Fix-memleaks-in-xmlXIncludeProcessFlags.patch
Patch2: Fix-memory-leaks-for-xmlACatalogAdd.patch
Patch3: Fix-memory-leaks-in-xmlACatalogAdd-when-xmlHashAddEntry-failed.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python3-devel
BuildRequires: zlib-devel
BuildRequires: pkgconfig
BuildRequires: xz-devel
BuildRequires: libtool
URL: http://xmlsoft.org/

%description
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Requires: zlib-devel
Requires: xz-devel
Requires: pkgconfig
Obsoletes: %{name}-static < %{version}-%{release}
Provides:  %{name}-static

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package -n python3-%{name}
Summary: Python 3 bindings for the libxml2 library
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}
Provides: %{name}-python3 = %{version}-%{release}

%description -n python3-%{name}
The libxml2-python3 package contains a Python 3 module that permits
applications written in the Python programming language, version 3, to use the
interface supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.

%package help
Summary:    Man page for libxml2
BuildArch:  noarch

%description  help
%{summary}.


%prep
%autosetup -n %{name}-%{version} -p1

mkdir py3doc
cp doc/*.py py3doc
sed -i 's|#!/usr/bin/python |#!%{__python3} |' py3doc/*.py

%build
./autogen.sh
%configure
%make_build

find doc -type f -exec chmod 0644 \{\} \;

%install
%configure --with-python=%{__python3}
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxml2-%{version}/*
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libxml2-python-%{version}/*
(cd doc/examples ; make clean ; rm -rf .deps Makefile)
gzip -9 -c doc/libxml2-api.xml > doc/libxml2-api.xml.gz

%check
make runtests

%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%doc %{_datadir}/doc/libxml2

%{_libdir}/lib*.so.*
%{_bindir}/xmllint
%{_bindir}/xmlcatalog

%files devel
%defattr(-, root, root)

%doc NEWS README.md Copyright
%doc doc/*.html doc/html doc/*.gif doc/*.png
%doc doc/tutorial doc/libxml2-api.xml.gz
%doc doc/examples
%doc %dir %{_datadir}/gtk-doc/html/libxml2
%doc %{_datadir}/gtk-doc/html/libxml2/*.devhelp2
%doc %{_datadir}/gtk-doc/html/libxml2/*.html
%doc %{_datadir}/gtk-doc/html/libxml2/*.png
%doc %{_datadir}/gtk-doc/html/libxml2/*.css

%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xml2-config
%{_datadir}/aclocal/libxml.m4
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/libxml2-config.cmake

%{_libdir}/*a

%files -n python3-%{name}
%defattr(-, root, root)

%{_libdir}/python3*/site-packages/libxml2.py*
%{_libdir}/python3*/site-packages/drv_libxml2.py*
%{_libdir}/python3*/site-packages/__pycache__/*py*
%{_libdir}/python3*/site-packages/libxml2mod*
%doc python/TODO
%doc python/libxml2class.txt
%doc py3doc/*.py
%doc doc/python.html

%files help
%doc %{_mandir}/man1/xml2-config.1*
%doc %{_mandir}/man1/xmllint.1*
%doc %{_mandir}/man1/xmlcatalog.1*
%doc %{_mandir}/man3/libxml.3*


%changelog
* Tue Sep 13 2022 fuanan <fuanan3@h-partners.com> - 2.9.14-2
- Fix Obsoletes in spec

* Wed Jul 13 2022 fuanan <fuanan3@h-partners.com> - 2.9.14-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:Upgrade to upstream v2.9.14 and Cleanup duplicate installation

* Fri Jun 24 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix memory leaks in xmlACatalogAdd when xmlHashAddEntry failed

* Thu Jun 16 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Fix memory leaks for xmlACatalogAdd

* Mon May 09 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-6
- Type:CVE
- ID:CVE-2022-29824
- SUG:NA
- DESC:fix CVE-2022-29824

* Wed Mar 09 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-5
- Type:CVE
- ID:CVE-2022-23308
- SUG:NA
- DESC:fix CVE-2022-23308

* Fri Feb 11 2022 fuanan <fuanan3@h-partners.com> - 2.9.12-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:use upstream patch refix heap-use-after-free in xmlAddNextSibling and xmlAddChild

* Fri Nov 12 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.12-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add backport bug fixes.
       work around lxml API abuse
       fix regression in xmlNodeDumpOutputInternal
       fix whitespace when serializing empty HTML documents
       forbid epsilon-reduction of final states
       fix buffering in xmlOutputBufferWrite

* Thu Nov 11 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.12-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix heap-use-after-free in xmlAddNextSibling and xmlAddChild

* Wed Nov 10 2021 Zhipeng Xie <xiezhipeng1@huawei.com> - 2.9.12-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:upgrade to upstream v2.9.12

* Tue Nov 9 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.10-19
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix memleaks in xmlXIncludeProcessFlags

* Sat Oct 30 2021 huangduirong <huangduirong@huawei.com> - 2.9.10-18
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix fuzz issues, fix null-deref in xmlSchemaGetComponentTargetNs

* Sat Oct 23 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.10-17
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix fuzz issues
       fix memory leaks in XPointer string-range function
       fix null pointer deref in xmlXPtrRangeInsideFunction
       stop using maxParserDepth in xpath.c
       hardcode maximum XPath recursion depth
       fix XPath recursion limit

* Thu Oct 21 2021 panxiaohe <panxiaohe@huawei.com> - 2.9.10-16
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix fuzz issues
       fix heap-use-after-free in xmlXIncludeIncludeNode
       fix stack overflow in xmlDocDumpMemory
       fix stack overflow in htmlDocContentDumpOutput

* Wed Jun 2 2021 guoxiaoqi <guoxiaoqi2@huawei.com> - 2.9.10-15
- Type:CVE
- ID:CVE-2021-3541
- SUG:NA
- DESC:fix CVE-2021-3541

* Sat May 29 2021 zoulin <zoulin13@huawei.com> - 2.9.10-14
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:[add] patches from upstream
       Fix-handling-of-unexpected-EOF-in-xmlParseContent.patch
       Fix-line-numbers-in-error-messages-for-mismatched-ta.patch
       Fix-null-deref-in-legacy-SAX1-parser.patch
       update-for-xsd-language-type-check.patch
       Fix-dangling-pointer-with-xmllint-dropdtd.patch
       Fix-duplicate-xmlStrEqual-calls-in-htmlParseEndTag.patch
       Fix-exponential-behavior-with-recursive-entities.patch
       Fix-quadratic-behavior-when-looking-up-xml-attribute.patch
       Fix-use-after-free-with-xmllint-html-push.patch
       Fix-xmlGetNodePath-with-invalid-node-types.patch
       Stop-checking-attributes-for-UTF-8-validity.patch

* Fri May 28 2021 guoxiaoqi <guoxiaoqi2@huawei.com> - 2.9.10-13
- Type:CVE
- ID:CVE-2021-3517, CVE-2021-3518
- SUG:NA
- DESC:fix CVE-2021-3517 and CVE-2021-3518

* Wed May 26 2021 yangkang <yangkang90@huawei.com> - 2.9.10-12
- Type:CVE
- ID:CVE-2021-3537
- SUG:NA
- DESC:fix CVE-2021-3537

* Tue Mar 2 2021 Lirui <lirui130@huawei.com> - 2.9.10-11
- fix problems detected by oss-fuzz test

* Thu Nov 12 2020 Liquor <lirui130@huawei.com> - 2.9.10-10
- fix problems detected by oss-fuzz test

* Thu Oct 29 2020 panxiaohe <panxiaohe@huawei.com> - 2.9.10-9
- remove subpackage python2-libxml2

* Mon Sep 14 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.9.10-8
- revert Don-t-try-to-handle-namespaces-when-building-HTML-do.patch.
  rubygem-nokogoro test case fail,because this patch remove xml namespace function.

* Thu Sep 10 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2.9.10-7
- Fixed some issues found in fuzzing testcases

* Fri Aug 28 2020 zoulin <zoulin13@huawei.com> - 2.9.10-6
- Fix more quadratic runtime issues in HTML push parse
- Fix reset HTML parser input before reporting error

* Wed Aug 12 2020 Liquor <lirui130@huawei.com> - 2.9.10-5
- Limit regexp nesting depth
- Fix exponential runtime in xmlFARecurseDeterminism

* Mon Aug 3 2020 Liquor <lirui130@huawei.com> - 2.9.10-4
- Fix integer overflow in xmlFAParseQuantExact

* Tue Jul 28 2020 shenyangyang <shenyangyang4@huawei.com> - 2.9.10-3
- Fix-use-after-free-with-validating-reader and
  Never-expand-parameter-entities-in-text-declaration

* Fri Jul 3 2020 wangchen <wangchen137@huawei.com> - 2.9.10-2
- Sync some patches from community

* Fri Apr 24 2020 BruceGW <gyl93216@163.com> - 2.9.10-1
- update upstream to 2.9.10

* Tue Mar 17 2020 Leo Fang<leofang_94@163.com> - 2.9.8-9
- Sync some patches from community 

* Thu Dec 19 2019 openEuler Buildteam <buildteam@openEuler.org> - 2.9.8-8
- Delete unused infomation

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.8-7
- Fix memory leak in xmlSchemaValidateStream

* Fri Sep 20 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.8-6
- Delete redundant information

* Tue Sep 10 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.8-5
- Delete epoch

* Thu Sep 5 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.8-2
- Backport upstream patches and merge static library to devel package

