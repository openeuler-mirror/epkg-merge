import os
import unittest
from src.transition.spec_writer import SpecWriter


class TestParse(unittest.TestCase):
    def setUp(self):
        self.spec_writer = SpecWriter(None, metadata={})

    def test_parse_config_settings(self):
        self.spec_writer.metadata = {"build.kconfig": {"ARCH": "x86", "CONFIG_PGO_KERNEL": "y"},
                                     "phase.prep": "%setup -q"}
        self.spec_writer.parse_config_settings()
        config_path = "arch/x86/configs/openeuler_defconfig"
        self.assertEqual(self.spec_writer.metadata["phase.prep"],
                         f"%setup -q{os.linesep}" + f"merge_config.sh -m {config_path} " \
                         "%{_sourcedir}/" + f"build.kconfig{os.linesep}mv .config {config_path} -f{os.linesep}")

    def test_format_meta(self):
        self.spec_writer.metadata = {"meta": {"summary": "this is a summary",
                                              "homepage": "https://xxx/111.tar.gz",
                                              "description": "this is a description"},
                                     "subpackage.glibc-all-langpacks": {"meta": {
                                              "summary": "this is a summary",
                                              "description": "this is a description"}}
                                     }
        expected_result = {'subpackage.glibc-all-langpacks': {
                               'summary': 'this is a summary',
                               'description': 'this is a description'},
                           'summary': 'this is a summary',
                           'homepage': 'https://xxx/111.tar.gz',
                           'description': 'this is a description'}
        self.spec_writer.format_meta()
        self.assertEqual(self.spec_writer.metadata, expected_result)

    def test_change_source_to_list(self):
        self.spec_writer.metadata = {'runtimePhase.post': "%do_post"}
        self.spec_writer.format_runtimePhase()
        self.assertEqual(self.spec_writer.metadata["post"], "%do_post")
        self.assertNotIn('runtimePhase.post', self.spec_writer.metadata)

    def test_merge_compile_flags(self):
        self.spec_writer.metadata = {"build.configure.flags": {
            "--enable-stack-protector": "strong",
            "--enable-tunables": True
        },
            "phase.configure": "./configure"}
        self.spec_writer.merge_compile_flags()
        self.assertEqual(self.spec_writer.target_metadata["rpmMacros"],
                         '%global build_configure_flags \\\n    --enable-stack-protector=strong \\\n    --enable-tunables\n')
        self.assertEqual(self.spec_writer.metadata["phase.configure"], '%{?add_configure_flags} ./configure')

    def test_parse_macros(self):
        self.spec_writer.metadata = {"rpmMacros": "%undefine __brp_ldconfi",
                                     "rpmGlobal": {
                                         "x86_arches": "%{ix86} x86_64"
                                     },
                                     "defineFlags": {
                                         "+docs": "",
                                         "-valgrind": ""
                                     }}
        self.spec_writer.parse_macros()
        self.assertEqual(self.spec_writer.target_metadata["rpmGlobal"], self.spec_writer.metadata["rpmGlobal"])
        self.assertEqual(self.spec_writer.target_metadata["defineFlags"],
                         {'': {'%bcond_without docs': '', '%bcond_with valgrind': ''}})

    def test_parse_phase(self):
        self.spec_writer.metadata = {
            "phase.prep": "%setup -q"}
        self.spec_writer.parse_phase()
        self.assertEqual(self.spec_writer.target_metadata["prep"], [{'condition': '', 'param': '', 'value': '%setup -q'}])

    def test_parse_subpackage(self):
        self.spec_writer.metadata = {
            "subpackage.glibc-common rpmWhen 0%{?xxx}": {"meta": {"summary": "xxx", "description": "xxx"},
                                                         "files rpmWhen 0%{?xxx}": "%docs"},
            "subpackage.glibc-devel": {"meta": {"summary": "xxx", "description": "xxx"},
                                       "files": "%docs"}}
        self.spec_writer.parse_subpackage()
        self.assertEqual(self.spec_writer.target_metadata["subpackage"],
                         {'glibc-common': {'rpmWhen 0%{?xxx}': {
                             'meta': {'': {'summary': 'xxx', 'description': 'xxx'}},
                             'files': {'rpmWhen 0%{?xxx}': '%docs'}}},
                          'glibc-devel': {'': {
                              'meta': {'': {'summary': 'xxx', 'description': 'xxx'}},
                              'files': {'': '%docs'}}}
                          })

    def test_print_value(self):
        input_text = "text\n%ifarch x86\ntext2"
        output_text = self.spec_writer.print_value(input_text)
        self.assertEqual(output_text, "text\n%ifarch x86\ntext2\n%endif\n")

    def test_print_endif(self):
        condition = "rpmWhen 0%{?xxx} rpmWhen 0%{?yyy}"
        output_text = self.spec_writer.print_endif(condition)
        self.assertEqual(output_text, '%endif\n%endif\n')

    def test_parse_when(self):
        k1 = "rpmWhen 0%{?fedora} >= 12 || 0%{?openEuler} >= 1"
        k2 = "rpmWhen 0%{?fedora} rpmWhen 0%{?openEuler}"
        expected_line = self.spec_writer.parse_when(k1)
        self.assertEqual(expected_line,
                         "%if 0%{?fedora} >= 12 || 0%{?openEuler} >= 1")
        expected_line = self.spec_writer.parse_when(k2)
        self.assertEqual(expected_line,
                         "%if 0%{?fedora} \n%if 0%{?openEuler}")
