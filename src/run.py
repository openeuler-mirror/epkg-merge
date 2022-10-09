# SPDX-License-Identifier: MulanPSL-2.0+
# Copyright (c) 2022 Huawei Technologies Co., Ltd. All rights reserved.

from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from app.app import Load, Get, Out


app = Flask(__name__)

app.debug = True
api = Api(app)
Swagger(app, Swagger.DEFAULT_CONFIG)
api.add_resource(Load, "/load_config")
api.add_resource(Get, "/get")
api.add_resource(Out, "/out")
