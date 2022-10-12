#!/usr/bin/python3
import ast

def validate_code(py_code) -> bool:
    try:
        ast.parse(py_code)
    except SyntaxError:
        print('Input isnt code.')
        return False
    print('Code is ok.')
    return True
