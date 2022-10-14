import os

import pytest

from src.core.config_space import config_space
from tests.src.core.loader.conftest import demo_dir


class TestLayerLoader:
    @pytest.mark.usefixtures("load_layer_and_destroy")
    def test_layer_loader(self):
        self._assert_all_pkgs()
        self._assert_libs()
        self._assert_use()
        self._assert_types()

    @classmethod
    def _assert_all_pkgs(cls):
        assert len(config_space.get("allPkgs")) == 4
        assert config_space.get("allPkgs") == {"python3", "less", "busybox", "kernel"}

        cls._assert_kernel()
        cls._assert_python3()
        cls._assert_busybox()
        cls._assert_less()

    @classmethod
    def _assert_libs(cls):
        assert len(config_space.get("libs")) == 3
        assert set(config_space.get("libs")) == {
            os.path.join(demo_dir, "layer", "libs", "calculate.py"),
            os.path.join(demo_dir, "layer", "libs", "exclusive_info.py"),
            os.path.join(demo_dir, "layer", "libs", "restart.py")
        }

    @classmethod
    def _assert_kernel(cls):
        fspath_list = config_space.get("pkgs.kernel:fspath")
        assert len(fspath_list) == 1
        fspath = fspath_list[0]
        assert fspath == os.path.join(demo_dir, "layer", "pkgs", "kernel", "kernel.yaml")
        assert config_space.get(f'files."{fspath}".name') == "kernel"
        assert config_space.get(f'files."{fspath}".docType') == "base"
        assert config_space.get(f'files."{fspath}".includePhase') == "phase.sh"
        assert config_space.get(f'files."{fspath}".includeRuntimePhase') == "runtime-phase.sh"
        assert config_space.get(f'files."{fspath}".include') == "versions.yaml files.yaml"
        assert config_space.get(f'files."{fspath}":referAttrs') == "types.package"
        assert config_space.get(f'files."{fspath}".meta:referAttrs') == "types.package.meta"
        assert config_space.get(f'files."{fspath}".phase:referAttrs') == "types.package.phase"
        assert config_space.get(f'files."{fspath}".runtimePhase:referAttrs') == "types.package.runtimePhase"

    @classmethod
    def _assert_python3(cls):
        fspath_list = config_space.get("pkgs.python3:fspath")
        assert len(fspath_list) == 2
        fspath = fspath_list[0]
        assert fspath == os.path.join(demo_dir, "layer", "pkgs", "python3", "python3.yaml")
        assert config_space.get(f'files."{fspath}".name') == "python3"
        assert config_space.get(f'files."{fspath}".docType') == "base"
        assert config_space.get(f'files."{fspath}".includePhase') == "phase.sh"
        assert config_space.get(f'files."{fspath}".includeRuntimePhase') == "runtime-phase.sh"
        assert config_space.get(f'files."{fspath}".include') == "versions.yaml files.yaml"
        assert config_space.get(f'files."{fspath}":referAttrs') == "types.package"
        assert config_space.get(f'files."{fspath}".meta:referAttrs') == "types.package.meta"
        assert config_space.get(f'files."{fspath}".phase:referAttrs') == "types.package.phase"
        assert config_space.get(f'files."{fspath}".runtimePhase:referAttrs') == "types.package.runtimePhase"

        fspath = fspath_list[1]
        assert fspath == os.path.join(demo_dir, "layer2", "pkgs", "python3", "python3.yaml")
        assert config_space.get(f'files."{fspath}".name') == "python3"
        assert config_space.get(f'files."{fspath}".docType') == "build"
        assert config_space.get(f'files."{fspath}".includePhase') == "phase.sh"
        assert config_space.get(f'files."{fspath}".includeRuntimePhase') == "runtime-phase.sh"
        assert config_space.get(f'files."{fspath}".include') == "versions.yaml files.yaml"
        assert config_space.get(f'files."{fspath}":referAttrs') == "types.package"
        assert config_space.get(f'files."{fspath}".meta:referAttrs') == "types.package.meta"
        assert config_space.get(f'files."{fspath}".phase:referAttrs') == "types.package.phase"
        assert config_space.get(f'files."{fspath}".runtimePhase:referAttrs') == "types.package.runtimePhase"

    @classmethod
    def _assert_busybox(cls):
        fspath_list = config_space.get("pkgs.busybox:fspath")
        assert len(fspath_list) == 1
        fspath = fspath_list[0]
        assert fspath == os.path.join(demo_dir, "layer_tools", "pkgs", "busybox", "busybox.yaml")
        assert config_space.get(f'files."{fspath}".name') == "busybox"
        assert config_space.get(f'files."{fspath}".includePhase') == "phase.sh"
        assert config_space.get(f'files."{fspath}".includeRuntimePhase') == "runtime-phase.sh"
        assert config_space.get(f'files."{fspath}".include') == "versions.yaml files.yaml"
        assert config_space.get(f'files."{fspath}":referAttrs') == "types.package"
        assert config_space.get(f'files."{fspath}".meta:referAttrs') == "types.package.meta"
        assert config_space.get(f'files."{fspath}".phase:referAttrs') == "types.package.phase"
        assert config_space.get(f'files."{fspath}".runtimePhase:referAttrs') == "types.package.runtimePhase"

    @classmethod
    def _assert_less(cls):
        fspath_list = config_space.get("pkgs.less:fspath")
        assert len(fspath_list) == 1
        fspath = fspath_list[0]
        assert fspath == os.path.join(demo_dir, "layer_tools", "pkgs", "less", "less.yaml")
        assert config_space.get(f'files."{fspath}".name') == "less"
        assert config_space.get(f'files."{fspath}".includePhase') == "phase.sh"
        assert config_space.get(f'files."{fspath}".includeRuntimePhase') == "runtime-phase.sh"
        assert config_space.get(f'files."{fspath}".include') == "versions.yaml files.yaml"
        assert config_space.get(f'files."{fspath}":referAttrs') == "types.package"
        assert config_space.get(f'files."{fspath}".meta:referAttrs') == "types.package.meta"
        assert config_space.get(f'files."{fspath}".phase:referAttrs') == "types.package.phase"
        assert config_space.get(f'files."{fspath}".runtimePhase:referAttrs') == "types.package.runtimePhase"

    @classmethod
    def _assert_use(cls):
        cls._assert_use_ssl()

    @classmethod
    def _assert_use_ssl(cls):
        fspath_list = config_space.get("use.ssl:fspath")
        assert len(fspath_list) == 1
        fspath = fspath_list[0]
        assert fspath == os.path.join(demo_dir, "layer_tools", "use", "ssl.yaml")
        assert config_space.get(f'use."{fspath}".name') == "ssl"
        assert config_space.get(f'use."{fspath}":referAttrs') == "types.use"
        assert config_space.get(f'use."{fspath}".meta:referAttrs') == "types.use.meta"

    @classmethod
    def _assert_types(cls):
        assert config_space.get("types.path:type") == "str"
        assert config_space.get("types.path:doc") == "filesystem path name"
        assert config_space.get("types.path:example") == "pkgs/bash/bash.yaml"
        assert config_space.get("types.path:checkFunc") == "is_path"
        assert config_space.get("types.path:mergeFunc") == "is_path"
        assert config_space.get("types.PATH:type") == "str"
        assert config_space.get("types.PATH:checkFunc") == "is_PATH"
        assert config_space.get("types.package:validSubkeys") == \
               "name version versions release meta source patchset requires buildRequires\nsubpackage phase " \
               "runtimePhase includePhase \nincludeRuntimePhase includeLib files use env\n"
        assert config_space.get("types.package.name:type") == "str"
        assert config_space.get("types.package.name:doc") == "package's spec_name"
        assert config_space.get("types.package.name:example") == "busybox"
        assert config_space.get("types.package.name:checkFunc") == "is_str"
        assert config_space.get("types.package.name:mergeFunc") == "merge_policy_first"
        assert config_space.get("types.package.epoch:type") == "int"
        assert config_space.get("types.package.epoch:checkFunc") == "is_between"
        assert config_space.get("types.package.epoch:checkParams") == "0,3"
        assert config_space.get("types.package.epoch:mergeFunc") == "merge_policy_first"
        assert config_space.get("types.package.version:type") == "str"
        assert config_space.get("types.package.version:checkFunc") == "is_version"
        assert config_space.get("types.package.version:mergeFunc") == "merge_policy_first"
        assert config_space.get("types.package.rpmMacros:type") == "list"
        assert config_space.get("types.package.rpmMacros:mergeFunc") == "merge_policy_first"
        assert config_space.get("types.package.release:type") == "str"
        assert config_space.get("types.package.release:checkFunc") == "is_release"
        assert config_space.get("types.package.release:mergeFunc") == "merge_policy_first"
        assert config_space.get("types.package.meta:type") == "str"
        assert config_space.get("types.package.phase:type") == "str"
        assert config_space.get("types.package.phase:mergeFunc") == "merge_policy_concat"
        assert config_space.get("types.package.phase:mergeParams") == "\n"
        assert config_space.get("types.package.includePhase:type") == "str"
        assert config_space.get("types.package.includePhase:mergeFunc") == "merge_policy_concat"
        assert config_space.get("types.package.includePhase:mergeParams") == "\n"
        assert config_space.get("types.package.source:type") == "str"
        assert config_space.get("types.package.source:mergeFunc") == "merge_policy_first"
        assert config_space.get("types.package.patchset:type") == "str"
        assert config_space.get("types.package.patchset:mergeFunc") == "merge_policy_first"
        assert config_space.get("types.package.buildRoot:type") == "list"
        assert config_space.get("types.package.buildRoot:mergeFunc") == "merge_policy_extend"
        assert config_space.get("types.package.buildRequires:type") == "list"
        assert config_space.get("types.package.buildRequires:mergeFunc") == "merge_policy_pre_extend"
        assert config_space.get("types.package.requires:type") == "list"
        assert config_space.get("types.package.requires:mergeFunc") == "merge_policy_pre_extend"
        assert config_space.get("types.package.files:type") == "str"
        assert config_space.get("types.package.files:mergeFunc") == "merge_policy_concat"
        assert config_space.get("types.package.files:mergeParams") == "\n"
