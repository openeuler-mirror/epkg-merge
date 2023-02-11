#!/usr/bin/python
# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

from setuptools import setup, find_packages

# python3 setup.py bdist_wheel
setup(
    name="merge-configs",
    version="0.0.4",
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
    ]
)
