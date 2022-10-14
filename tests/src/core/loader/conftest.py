import os

import pytest

from src.core.config_space import config_space
from src.core.loader.layer_loader import LayerLoader

demo_dir = os.path.abspath(os.path.join(os.path.abspath(os.curdir), "../../../demo"))


@pytest.fixture
def load_layer_and_destroy():
    config_file = os.path.join(demo_dir, "config.yaml")
    LayerLoader(config_file).load()
    yield
    config_space.clear()
