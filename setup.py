#!/usr/bin/python
# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

import os
from setuptools import setup, find_packages
from src.etc import etc_path
from src.transition.template import template_path

data_files = []
target_dirs = {
    "src/etc": etc_path,
    "src/transition/template": template_path
}


def get_file_paths(prefix, directory):
    for name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, name)):
            get_file_paths(os.path.join(prefix, name), os.path.join(directory, name))
        elif name.endswith(".py"):
            continue
        else:
            data_files.append(os.path.join(prefix, name))


for rel_path, target_dir in target_dirs.items():
    get_file_paths(rel_path, target_dir)

# python3 setup.py bdist_wheel
setup(
    name="merge-configs",
    version="0.1.2",
    packages=find_packages(),
    description="...",
    license="MulanPSL-2.0+",
    author="",
    entry_points={
        "console_scripts": [
            'merge-configs = src.merge_configs:main'
        ]
    },
    include_package_data=True,
    install_requires=[
        'PyYAML>=3.0',
        'Cheetah3==3.2.6.post2',
        'ply>=3.11'
    ],
    data_files=[
        ("", data_files),
    ],
)
