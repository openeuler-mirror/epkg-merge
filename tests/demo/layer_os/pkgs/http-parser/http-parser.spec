Name:           http-parser
Version:        2.9.4
Release:        2
Summary:        HTTP request/response parser for C

License:        MIT
URL:            https://github.com/nodejs/%{name}
Source0:        https://github.com/nodejs/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch6000:      backport-url-treat-empty-port-as-default.patch

BuildRequires:  gcc meson

%description
http-parser parses the HTTP request headers and body. As such, it acts as
a barrier in the policy to guarantee that the entire content has been received
before any other filters are invoked.The parser filter forces the server
to do "store-and-forward" routing instead of the default "cut-through" routing,
where the request is only parsed on-demand. This filter can be used as a simple test
to ensure that the message is XML, for example.

Features:

  * No dependencies
  * Handles persistent streams (keep-alive)
  * Decodes chunked encoding
  * Upgrade support
  * Defends against buffer overflow attacks

%package devel
Summary: Development headers and static libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development headers and static libraries for http-parser.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

cat > meson.build << EOF
project('%{name}', 'c',
        version : '%{version}',
        license: 'MIT')

install_headers('http_parser.h')
foreach x : [['http_parser',        ['-DHTTP_PARSER_STRICT=0']],
             ['http_parser_strict', ['-DHTTP_PARSER_STRICT=1']]]

  lib = library(x.get(0), 'http_parser.c', c_args : x.get(1),
                version : '%{version}', install : true)

  test('test-@0@'.format(x.get(0)),
       executable('test-@0@'.format(x.get(0)), 'test.c',
                  c_args : x.get(1), link_with : lib),
                  timeout : 60)
endforeach
EOF

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test
%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so

%files help
%defattr(-,root,root)
%doc AUTHORS README.md

%changelog
* Mon Jul 25 2022 yanglu <yanglu72@h-partners.com> - 2.9.4-2
- Include patch to work colon but no port

* Tue Jun 23 2020 hanzhijun <hanzhijun1@huawei.com> - 2.9.4-1
- update to 2.9.4

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 2.9.2-2
- optimization the patch

* Sat Aug 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.9.2-1
- Package init
