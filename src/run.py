# Copyright (c) 2022 Huawei Technologies Co.,Ltd. All rights reserved.
#
# StratoVirt is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan
# PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http:#license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

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
