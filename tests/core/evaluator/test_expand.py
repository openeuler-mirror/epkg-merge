import unittest
from unittest.mock import patch

from src.core.evaluator.expand import expand_macro


class TestExpand(unittest.TestCase):
    # @patch("src.core.config_space.config_space.get_key", return_value="unittest")
    # def test_expand_macro(self, mock_config_space_get):
    #     str_macro = """1%%a 2%%{b}3%%%c 4%%%{d}5unittest 6unittest 7unittest
    #     8%%ab"""
    #     expectation = """1unittest 2unittest3unittest 4unittest5unittest 6unittest 7unittest
    #     8unittest"""
    #     res = expand_macro(str_macro, "")
    #     print(res)
    #     self.assertEqual(res, expectation)

    @patch("src.core.config_space.config_space.get_key")
    def test_expand_version_not_equal(self, mock_config_space_get):
        mock_config_space_get.return_value = "4.2.1"
        str_macro = r"@4.20.1"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "False")

    @patch("src.core.config_space.config_space.get_key")
    def test_expand_version_equal(self, mock_config_space_get):
        mock_config_space_get.return_value = "4.2.1"
        str_macro = r"@4.2.1"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "True")

    @patch("src.core.config_space.config_space.get_key")
    def test_expand_version_ge(self, mock_config_space_get):
        mock_config_space_get.return_value = "4.2.1"
        str_macro = r"@4.2.1:"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "True")
        str_macro = r"@4.1.1:"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "True")
        str_macro = r"@4.3.1:"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "False")

    @patch("src.core.config_space.config_space.get_key")
    def test_expand_version_le(self, mock_config_space_get):
        mock_config_space_get.return_value = "4.2.1"
        str_macro = r"@:4.2.1"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "True")
        str_macro = r"@:4.1.1"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "False")
        str_macro = r"@:4.3.1"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "True")

    @patch("src.core.config_space.config_space.get_key")
    def test_expand_version_le_ge(self, mock_config_space_get):
        mock_config_space_get.return_value = "4.2.1"
        str_macro = r"@4.2.1:4.2.1"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "True")
        str_macro = r"@4.0.1:4.1.1"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "False")
        str_macro = r"@4.1.1:4.3.1"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "True")

    @patch("src.core.config_space.config_space.get_key")
    def test_expand_value_not_when(self, mock_config_space_get):
        mock_config_space_get.return_value = "4.2.1"
        str_macro = r"@4.2.1:4.2.1"
        res = expand_macro(str_macro, "", False)
        self.assertEqual(res, str_macro)


    def test_expand_pkg(self):
        from src.core.config_space import config_space
        config_space["pkgs.kernel.rpmGlobal.dd"] = "4.2.1"
        str_macro = r"${{pkg.rpmGlobal.dd}}"
        config_space[f"files.\"\".cspath"] =  "pkgs.kernel"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "4.2.1")

    def test_expand_rpmGlobal(self):
        from src.core.config_space import config_space
        config_space["rpmGlobal.dd"] = "4.2.1"
        str_macro = r"${{rpmGlobal.dd}}"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "4.2.1")

    def test_expand_rpmrc(self):
        from src.core.config_space import config_space
        config_space["rpmGlobal.cc"] = "4.2.1"
        str_macro = r"${{rpmrc.cc}}"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "4.2.1")


    def test_expand_top(self):
        from src.core.config_space import config_space
        config_space["pkgs.kernel.cc"] = "4.2.1"
        str_macro = r"${{top.pkgs.kernel.cc}}"
        res = expand_macro(str_macro, "", True)
        self.assertEqual(res, "4.2.1")