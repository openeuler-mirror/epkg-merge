import unittest
from src.core.interpreter.interpreter import call, startup

class TestExpand(unittest.TestCase):
    def test_call(self):
        py_caode = 'math.sqrt(4)'
        expectation = 2.0
        result = call(py_caode)
        print(result)
        self.assertEqual(result, expectation)
