import os

import pytest

from src.core.config_space import config_space
from src.core.loader.layer_loader import LayerLoader
file_path = os.path.abspath(__file__)
file_dir, _ = os.path.split(file_path)
demo_dir = os.path.abspath(os.path.join(file_dir, "../../../tests/demo"))

@pytest.fixture
def load_layer_and_destroy():
    config_file = os.path.join(demo_dir, "config.yaml")
    LayerLoader(config_file).load()
    yield
    config_space.clear()
