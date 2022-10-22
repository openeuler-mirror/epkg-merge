import unittest

from unittest.mock import patch

from src.core.evaluator.expand import expand_macro


class TestExpand(unittest.TestCase):
    @patch("src.core.config_space.config_space.get_key", return_value="unittest")
    def test_expand_macro(self, mock_config_space_get):
        str_macro = """1%%a 2%%{b}3%%%c 4%%%{d}5d.d 6dd.e.a.b 7dd.f.a.d
        8%%ab"""
        expectation = """1unittest 2unittest3unittest 4unittest5unittest 6unittest 7unittest
        8unittest"""
        res = expand_macro(str_macro)
        print(res)
        self.assertEqual(res, expectation)
