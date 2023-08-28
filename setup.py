#!/usr/bin/python
# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

from setuptools import setup, find_packages

# python3 setup.py bdist_wheel
setup(
    name="merge-configs",
    version="0.1.0",
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
        ("", ["src/transition/template/meta.tmpl",
              "src/transition/template/spec.tmpl",
              "src/transition/template/add_configure.tmpl"]),
    ],
)
