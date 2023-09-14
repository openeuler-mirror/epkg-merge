import unittest
import yaml
from unittest.mock import patch
import os

from src.core.evaluator.expand import expand_macro
from src.core.evaluator.merge import is_when
from src.core.loader.layer_loader import LayerLoader
from src.core.config_space import config_space
from src.core.interpreter.interpreter import StartUp


def save_config(config):
    with open(f"./_layers/config.yaml", "w") as f:
        yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

        def repr_str(dumper, data):
            if '\n' in data:
                return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
            return dumper.org_represent_str(data)

        yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)
        yaml.safe_dump(config, f, allow_unicode='uft-8', sort_keys=False)
        f.close()


def init(package, arch):
    current_dir = os.path.abspath(os.curdir)
    config_file = os.path.join(current_dir, "_layers/config.yaml")
    LayerLoader(config_file).load(arch)
    StartUp.startup(config_space)
    config_space.set_arch(arch)
    return config_space.get_package_format_json(package)


config = {
    "layers": [
        "base",
        "custom"
    ]
}


class TestExpand(unittest.TestCase):

    def test_merge_version(self):
        save_config(config)
        pacakge_json = init("redis", "aarch64")
        version = pacakge_json.get("version")
        self.assertEqual(version, "4.0.15")

    def test_merge_when_version(self):
        # when @xxxx
        save_config(config)
        pacakge_json = init("redis", "aarch64")
        patchset = pacakge_json.get("patchset")
        self.assertEqual(list(patchset.keys()), ['3'])

    def test_merge_defineFlags(self):
        # when defineFlags.+ and defineFlags.-
        save_config(config)
        pacakge_json = init("redis", "aarch64")
        source = pacakge_json.get("source")
        self.assertEqual(source.get("5"), "plus.patch")
        self.assertEqual(source.get("6"), None)

    @patch("src.core.config_space.config_space.get_key")
    def test_is_when(self, mock_config_space_get):
        mock_config_space_get.return_value = "4.2.1"
        str_macro = r"(${{ top.pkgs.kernel.version }} <= 4.5.2)"
        item = {
            "fspath": "",
            "when": str_macro
        }
        res = is_when(item)
        self.assertEqual(res, True)
