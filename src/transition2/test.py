import unittest
from src.transition2.yaml2spec import SpecWriter


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.spec_writer = SpecWriter(None, {})

    def test_parse_files(self):
        self.spec_writer.metadata = \
            {'name': 'glibc', 'files': '#:rpm_macro_param: -f file.list\nline1\nline2\n',
             'files when +gcc': 'line1\nline2\n',
             'subpackage.common': {'files': '#:rpm_macro_param: -f common\nline1\nline2\n'},
             'subpackage.glibc-devel': {'files': 'devel\nline1\n'},
             'subpackage.glibc-compat-2.17 when +compat_2_17': {'files': '#:rpm_macro_param: -f compat-2.17.filelist\n'}
             }
        self.spec_writer.parse_files1()
        self.spec_writer.trans_data_to_spec('spec.tmpl')

    def test_parse_macros(self):
        self.spec_writer.metadata = \
            {'rpmMacros': 'line1\nline2\n',
             'rpmGlobal': {'atk_version': '2.13.1', 'glib2_version': '2.49.4'},
             'useFlags': {'+valgrind': '', '-benchtests': ''},
             'useFlags when arch in %{valgrind_arches}': {'-valgrind': ''}
             }
        self.spec_writer.parse_macros()
        self.spec_writer.trans_data_to_spec('macros.tmpl')

    def test_parse_meta(self):
        self.spec_writer.metadata = \
            {'meta': {'summary': 'Interpreter of the Python3 programming language',
                      'license': 'Python-2.0',
                      'homepage': 'https://www.python.org/',
                      'group': '',
                      'description': 'Python combines remarkable power with very clear syntax. It has modules,\n'
                                     'classes, exceptions, very high level dynamic data types, and dynamic\n'
                                     'typing. There are interfaces to many system calls and libraries, as well\n'
                                     'as to various windowing systems. New built-in modules are easily written\n'
                                     'in C or C++ (or other languages, depending on the chosen implementation).\n'
                                     'Python is also usable as an extension language for applications written\n'
                                     'in other languages that need easy-to-use scripting or automation interfaces.\n\n'
                                     'This package Provides python version 3.\n'}}
        self.spec_writer.parse_meta()
        self.spec_writer.parse_str_keys()
        self.spec_writer.trans_data_to_spec('meta.tmpl')

    def test_str_keys(self):
        self.spec_writer.metadata = \
            {'meta': {'summary': 'Interpreter of the Python3 programming language',
                      'license': 'Python-2.0',
                      'homepage': 'https://www.python.org/',
                      'group': 'system',
                      'description': 'Python combines remarkable power with very clear syntax. It has modules,\n'
                                     'classes, exceptions, very high level dynamic data types, and dynamic\n'
                                     'typing. There are interfaces to many system calls and libraries, as well\n'
                                     'as to various windowing systems. New built-in modules are easily written\n'
                                     'in C or C++ (or other languages, depending on the chosen implementation).\n'
                                     'Python is also usable as an extension language for applications written\n'
                                     'in other languages that need easy-to-use scripting or automation interfaces.\n\n'
                                     'This package Provides python version 3.\n'},
             'name': 'python3',
             'version': '3.10.2',
            }
        self.spec_writer.parse_meta()
        self.spec_writer.parse_str_keys()
        self.spec_writer.trans_data_to_spec('spec.tmpl')