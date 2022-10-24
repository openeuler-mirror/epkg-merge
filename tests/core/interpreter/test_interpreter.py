import unittest
from src.core.interpreter import interpreter


class TestExpand(unittest.TestCase):
    def test_call(self):
        startup_status = interpreter.StartUp.startup('').get('startup_status')
        expectation = {
            'code': 'cal_sqrt(4)',
            'legality': True,
            'result': 2.0
        }
        if startup_status:
            from src.core.interpreter import executor
            py_code = 'cal_sqrt(4)'
            result = executor.call(py_code)
            self.assertEqual(result, expectation)

