# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.


class LayerLoader():
    # 避免模块的循环依赖
    from src.core.config_space import config_space
    pass