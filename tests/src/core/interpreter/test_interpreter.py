import unittest
from src.core.interpreter import interpreter

class TestExpand(unittest.TestCase):
    def test_call(self):
        interpreter.StartUp().startup('')
        py_code = 'cal_sqrt(4)'
        expectation = {
            'code': 'cal_sqrt(4)',
            'legality': True,
            'result': 2.0
        }
        from src.core.interpreter import executor
        result = executor.call(py_code)
        self.assertEqual(result, expectation)
