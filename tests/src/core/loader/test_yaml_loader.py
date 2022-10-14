import pytest

from src.core.config_space import config_space


class TestYamlLoader:
    @pytest.mark.usefixtures("load_layer_and_destroy")
    def test_yaml_loader_pkg(self):
        assert config_space.get_key("pkgs.kernel.name") == "kernel%{?package64kb}"
        assert len(config_space.get_key("pkgs.kernel:loadedKeys")) == 78

    @pytest.mark.usefixtures("load_layer_and_destroy")
    def test_yaml_loader_use(self):
        assert config_space.get_key("use.ssl.doc") == "description-ssl"
        assert len(config_space.get_key("use.ssl:loadedKeys")) == 7
