import os
import unittest
from src.transition.spec_writer import SpecWriter


class TestParse(unittest.TestCase):
    def setUp(self):
        self.spec_writer = SpecWriter(None, metadata={})

    def test_parse_patchset(self):
        self.spec_writer.metadata = {"patchset": ["patch1", {"patch2": "-p2"}, ["patch3", "-p3"]]}
        self.spec_writer.parse_patchset()
        self.assertEqual(self.spec_writer.metadata["patchset"], ["patch1", "patch2", "patch3"])
        self.assertEqual(self.spec_writer.metadata["PatchOpts"], ["-p1", "-p2", "-p3"])

    def test_change_subpackage_to_list(self):
        self.spec_writer.metadata = {"subpackage": {"subpackage1": {"key1": "value1"}, "subpackage2": {"key2": "value2"}}}
        expected_result = [{"name": "subpackage1", "asWholeName": True, "key1": "value1"},
                                {"name": "subpackage2", "asWholeName": True, "key2": "value2"}]
        self.spec_writer.change_subpackage_to_list()
        self.assertEqual(self.spec_writer.metadata["subpackage"], expected_result)

    def test_change_source_to_list(self):
        self.spec_writer.metadata = {'source': {'source1': 'url1', 'source2': 'url2'}}
        expected_result = ['url1', 'url2']
        self.spec_writer.change_source_to_list()
        self.assertEqual(self.spec_writer.metadata["source"], expected_result)

    def test_change_rpmmacros_linesep(self):
        self.spec_writer.metadata = {"rpmMacros": ["macro1{os.linesep}", "macro2"]}
        expected_result = ["macro1\n", "macro2"]
        self.spec_writer.change_rpmmacros_linesep()
        self.assertEqual(self.spec_writer.metadata["rpmMacros"], expected_result)

    def test_generate_necessary_keys(self):
        self.spec_writer.metadata = {}
        self.spec_writer.generate_necessary_keys()
        expected_keys = ["name", "version", "meta.summary", "meta.license", "release", "meta.description", "builder"]
        for key in expected_keys:
            self.assertIn(key, self.spec_writer.metadata.keys())

        self.spec_writer.metadata = {"name": "test", "version": "1.0"}
        self.spec_writer.generate_necessary_keys()
        expected_keys = ["meta.summary", "meta.license", "release", "meta.description", "builder"]
        for key in expected_keys:
            self.assertIn(key, self.spec_writer.metadata.keys())

    def test_change_field(self):
        metadata = {
            "rpmWhen test": "test",
            "runtimePhase.test": {
                "phase.test": {
                    "meta.test": "test"
                }
            }
        }
        expected_metadata = {
            "test": "test",
            "test": {
                "test": {
                    "test": "test"
                }
            }
        }
        self.spec_writer.metadata = metadata
        self.spec_writer.change_field()
        self.assertEqual(self.spec_writer.metadata, expected_metadata)

    def test_parse_subpackage_files_with_if(self):
        metadata = {
            "subpackage": [
                {
                    "files%if condition": ["file1", "file2"],
                    "other_key": "other_value"
                }
            ]
        }
        expected_metadata = {
            "subpackage": [
                {
                    "filesJudgement": ["%if condition"],
                    "files": ["file1", "file2"],
                    "other_key": "other_value"
                }
            ]
        }
        self.spec_writer.metadata = metadata
        self.spec_writer.parse_subpackage_files_with_if()
        self.assertEqual(self.spec_writer.metadata, expected_metadata)

    def test_parse_special_key(self):
        self.spec_writer.metadata = {
            'buildRequires': ["m %if a", "n %else %if a %if b"]
        }
        self.spec_writer.parse_special_key()
        expected_special_key = "%if a\nbuildRequires: m \n%endif\n\n%if b\n%if a " \
                               "\n%else\nbuildRequires: n \n%endif\n%endif\n\n"
        self.assertEqual(self.spec_writer.metadata["SpecialKey"], expected_special_key)