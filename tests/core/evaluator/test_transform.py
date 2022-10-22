import unittest

from src.core.evaluator.transform import parse_shell_file, transform_key_with_when


class TestExpand(unittest.TestCase):
    def test_parse_shell_file(self):
        file_content = '''
#!/bin/bash

public_network_ok()
{
        ping -c 1 -W 10 114.114.114.114 >/dev/null 2>&1 ||
                curl -k -s -m 10 --retry-delay 2 --retry 5 https://compass-ci.openeuler.org/ -o /dev/null
}
echo "--"
test_a() {
        echo "test_a"
}

test_b(){
        echo "test_b"
}

function test_c() {
        echo "test_c"
}

function test_d(){
        echo "test_d"
}

function test_e()
{
        echo "test_e"
}

function test_f {
        echo "test_f"
}

function test_g{
        echo "test_g"
}

function test_h
{
        echo "test_h"
}
        '''
        expectation = {
            'public_network_ok': '        ping -c 1 -W 10 114.114.114.114 >/dev/null 2>&1 '
                                 '||\n'
                                 '                curl -k -s -m 10 --retry-delay 2 '
                                 '--retry 5 https://compass-ci.openeuler.org/ -o '
                                 '/dev/null\n',
            'test_a': '        echo "test_a"\n',
            'test_b': '        echo "test_b"\n',
            'test_c': '        echo "test_c"\n',
            'test_d': '        echo "test_d"\n',
            'test_e': '        echo "test_e"\n',
            'test_f': '        echo "test_f"\n',
            'test_g': '        echo "test_g"\n',
            'test_h': '        echo "test_h"\n'
        }
        res = parse_shell_file(file_content.splitlines(keepends=True))
        self.assertEqual(res, expectation)

    def test_transform_key_with_when(self):
        k1 = "patch.1 when +ssl"
        k2 = "patch.1 when ssl"
        k3 = "patch.1 when -ssl"
        value = "test"
        fspath = "fspath"
        k, v = transform_key_with_when(k1, value, fspath)
        self.assertEqual(k, "patch.1")
        self.assertEqual(v, {'value': 'test', 'fspath': 'fspath', 'when': '%%use.ssl'})
        k, v = transform_key_with_when(k2, value, fspath)
        self.assertEqual(k, "patch.1")
        self.assertEqual(v, {'value': 'test', 'fspath': 'fspath', 'when': '%%use.ssl'})
        k, v = transform_key_with_when(k3, value, fspath)
        self.assertEqual(k, "patch.1")
        self.assertEqual(v, {'value': 'test', 'fspath': 'fspath', 'when': '{{ not %%use.ssl }}'})
