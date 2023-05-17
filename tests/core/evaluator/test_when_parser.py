import unittest
# from when_parser import parse
from src.core.evaluator.parser.when_parser import parser

class TestWhenParser(unittest.TestCase):    
    def test_parse_equals(self):
        self.assertEqual(parser.parse("2022-01-01 == 2022-01-01"), True)
        self.assertEqual(parser.parse("2022-01-01 == 2022-01-02"), False)

        
    def test_parse_true_false(self):
        self.assertEqual(parser.parse("True"), True)
        self.assertEqual(parser.parse("False"), False)

        
    def test_parse_in(self):
        self.assertEqual(parser.parse("arch64 in arch64 arm64"), True)
        self.assertEqual(parser.parse("x86 in arch64 arm64"), False)
        
    def test_parse_not_in(self):
        self.assertEqual(parser.parse("arch not in a b"), True)
        self.assertEqual(parser.parse("arch not in arch a"), False)

    
    def test_parse_comparison(self):
        self.assertEqual(parser.parse("11 > 12"), False)
        self.assertEqual(parser.parse("11 < 12"), True)
        self.assertEqual(parser.parse("11 <= 11"), True)
        self.assertEqual(parser.parse("12 >= 12"), True)
        self.assertEqual(parser.parse("11 != 12"), True)
        self.assertEqual(parser.parse("a != a"), False)
        self.assertEqual(parser.parse("a == a"), True)
        self.assertEqual(parser.parse("a == b"), False)
        self.assertEqual(parser.parse("a = a"), True)
        self.assertEqual(parser.parse("a = b"), False)

        
    def test_parse_logical(self):
        self.assertEqual(parser.parse("True and True"), True)
        self.assertEqual(parser.parse("True and False"), False)
        self.assertEqual(parser.parse("False and True"), False)
        self.assertEqual(parser.parse("False and False"), False)
        self.assertEqual(parser.parse("True or True"), True)
        self.assertEqual(parser.parse("True or False"), True)
        self.assertEqual(parser.parse("False or True"), True)
        self.assertEqual(parser.parse("False or False"), False)
        self.assertEqual(parser.parse("not True"), False)
        self.assertEqual(parser.parse("not False"), True)
        self.assertEqual(parser.parse("not 1"), False)
        self.assertEqual(parser.parse("not 0"), True)
        self.assertEqual(parser.parse("True && True"), True)
        self.assertEqual(parser.parse("True && False"), False)
        self.assertEqual(parser.parse("False && True"), False)
        self.assertEqual(parser.parse("False && False"), False)
        self.assertEqual(parser.parse("True || True"), True)
        self.assertEqual(parser.parse("True || False"), True)
        self.assertEqual(parser.parse("False || True"), True)
        self.assertEqual(parser.parse("False || False"), False)
        self.assertEqual(parser.parse("!True"), False)
        self.assertEqual(parser.parse("!False"), True)
        self.assertEqual(parser.parse("!1"), False)
        self.assertEqual(parser.parse("!0"), True)

        
    def test_parse_logical_combination(self):
        self.assertEqual(parser.parse("True and False or True"), True)
        self.assertEqual(parser.parse("True and False or False"), False)
        self.assertEqual(parser.parse("False and True or True"), True)
        self.assertEqual(parser.parse("False and True or False"), False)
        self.assertEqual(parser.parse("not True and False or True"), True)
        self.assertEqual(parser.parse("not True and False or False"), False)
        self.assertEqual(parser.parse("not False and True or True"), True)
        self.assertEqual(parser.parse("not False and True or False"), True)
        self.assertEqual(parser.parse("not True or False and True"), False)
        self.assertEqual(parser.parse("not True or False and False"), False)
        self.assertEqual(parser.parse("not False or True and True"), True)
        self.assertEqual(parser.parse("not False or True and False"), False)
        self.assertEqual(parser.parse("not True and not False or True"), True)
        self.assertEqual(parser.parse("not True and not False or False"), False)
        self.assertEqual(parser.parse("not False and not True or True"), True)
        self.assertEqual(parser.parse("not False and not True or False"), False)
        self.assertEqual(parser.parse("not True or not False and True"), True)
        self.assertEqual(parser.parse("not True or not False and False"), False)
        self.assertEqual(parser.parse("not False or not True and True"), True)
        self.assertEqual(parser.parse("not False or not True and False"), False)

    
    def test_parse_parentheses(self):
        self.assertEqual(parser.parse("(True and False) or True"), True)
        self.assertEqual(parser.parse("True and (False or False)"), False)
        self.assertEqual(parser.parse("False and (True or True)"), False)
        self.assertEqual(parser.parse("False and (True or False)"), False)
        self.assertEqual(parser.parse("not (True and False) or True"), True)
        self.assertEqual(parser.parse("not (True and False) or False"), True)
        self.assertEqual(parser.parse("not (False and True) or True"), True)
        self.assertEqual(parser.parse("not (False and True) or False"), True)
        self.assertEqual(parser.parse("not True or (False and True)"), False)
        self.assertEqual(parser.parse("not True or (False and False)"), False)
        self.assertEqual(parser.parse("not False or (True and True)"), True)
        self.assertEqual(parser.parse("not False or (True and False)"), True)
        self.assertEqual(parser.parse("not (True and not False) or True"), True)
        self.assertEqual(parser.parse("not (True and not False) or False"), False)
        self.assertEqual(parser.parse("not (False and not True) or True"), True)
        self.assertEqual(parser.parse("not (False and not True) or False"), True)
        self.assertEqual(parser.parse("not True or not (False and True)"), True)
        self.assertEqual(parser.parse("not True or not (False and False)"), True)
        self.assertEqual(parser.parse("not False or not (True and True)"), True)
        self.assertEqual(parser.parse("not False or not (True and False)"), True)




if __name__ == '__main__':
    unittest.main()