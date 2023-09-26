import unittest

from src.core.evaluator.transform import parse_shell_file, transform_key_with_when, parse_file_name, \
    transform_key_default, transform_key_with_rpmWhen


class TestExpand(unittest.TestCase):
    def test_parse_shell_file(self):
        file_content = '''
#!/bin/bash

public_network_ok() {
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

function test_e() {
        echo "test_e"
}

function test_f {
        echo "test_f"
}

function test_g{
        echo "test_g"
}

function test_h{
        echo "test_h"
}

post:%{wxbasename}-devel(){
        echo "subpackage"
}
        '''
        expectation = {
            'runtimePhase.public_network_ok': '        ping -c 1 -W 10 114.114.114.114 >/dev/null 2>&1 ||\n'
                                              '                curl -k -s -m 10 --retry-delay 2 --retry 5 '
                                              'https://compass-ci.openeuler.org/ -o /dev/null\n',
            'runtimePhase.test_a': '        echo "test_a"\n',
            'runtimePhase.test_b': '        echo "test_b"\n',
            'runtimePhase.test_c': '        echo "test_c"\n',
            'runtimePhase.test_d': '        echo "test_d"\n',
            'runtimePhase.test_e': '        echo "test_e"\n',
            'runtimePhase.test_f': '        echo "test_f"\n',
            'runtimePhase.test_g': '        echo "test_g"\n',
            'runtimePhase.test_h': '        echo "test_h"\n',
            "subpackage.%{wxbasename}-devel.runtimePhase.post": '        echo '
                                                                '"subpackage"\n'
        }
        res = parse_shell_file("runtimePhase", file_content.splitlines(keepends=True))
        for k,v in res.items():
            print(k)
            self.assertEqual(res[k], expectation[k])

    def test_transform_key_with_when(self):
        k1 = "patch.1 when +ssl"
        k2 = "patch.1 when ssl"
        k3 = "patch.1 when -ssl"
        value = {
            "value": "test",
            "fspath": "fspath"
        }
        res = transform_key_with_when({k1: value})
        self.assertEqual(res, {'patch.1': {'fspath': 'fspath', 'value': 'test', 'when': '%%use.ssl'}})
        res = transform_key_with_when({k2: value})
        self.assertEqual(res, {'patch.1': {'fspath': 'fspath', 'value': 'test', 'when': '%%use.ssl'}})
        res = transform_key_with_when({k3: value})
        self.assertEqual(res, {'patch.1': {'fspath': 'fspath', 'value': 'test', 'when': '{{ not %%use.ssl }}'}})

    def test_parse_file_name(self):
        file = "/tmp/xxx/runtimePhase.sh"
        file_name = parse_file_name(file)
        self.assertEqual(file_name, "runtimePhase")

    def test_transform_key_default(self):
        key = "subpackage.help rpmWhen %ifarch %{arm}.summary"
        res = transform_key_default(key, "test", "fs")
        expectation = {'subpackage.help.summary': {'value': 'test', 'fspath': 'fs', 'when': None},
                       'subpackage.help:rpmWhen': {'value': '%ifarch %{arm}', 'fspath': 'fs', 'when': None}}
        self.assertEqual(res, expectation)

    def test_transform_key_with_rpmWhen(self):
        k1 = "subpackage.python2-perf rpmWhen %{with_perf} rpmWhen 0%{?with_python2}.meta.summary rpmWhen %{with_perf}"
        k2 = "subpackage.python2-perf rpmWhen %{with_perf} rpmWhen 0%{?with_python2} rpmWhen 0%{?with_python3}.meta.summary"
        k3 = "subpackage.python2-perf.files rpmWhen %{with_perf}"
        value = {
            "value": "test",
            "fspath": "fspath"
        }
        res = transform_key_with_rpmWhen({k1: value})
        self.assertEqual(res, {'subpackage.python2-perf.meta.summary': {'fspath': 'fspath', 'value': 'test'},
                               'subpackage.python2-perf:rpmWhen %{with_perf} rpmWhen 0%{?with_python2}':
                                   {'value': 'test', 'fspath': 'fspath'}})
        res = transform_key_with_rpmWhen({k2: value})
        self.assertEqual(res, {'subpackage.python2-perf.meta.summary': {'fspath': 'fspath', 'value': 'test'},
                               'subpackage.python2-perf:rpmWhen %{with_perf} rpmWhen 0%{?with_python2} rpmWhen 0%{?with_python3}':
                                   {'value': 'test','fspath': 'fspath'}
                               })
        res = transform_key_with_rpmWhen({k3: value})
        self.assertEqual(res, {'subpackage.python2-perf.files': {'fspath': 'fspath', 'value': 'test'},
                               'subpackage.python2-perf.files:rpmWhen %{with_perf}':
                                   {'fspath': 'fspath', 'value': 'test'}})
