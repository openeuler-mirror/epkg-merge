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

from jsonschema.validators import validate
from functools import wraps
from jsonschema.exceptions import SchemaError, ValidationError

import flask
from flask import request
from flask_restful import Resource

def api_response_handler(fn):
    """
    api装饰器, 生产统一风格的返回体
    {
        "code": 0,
        "data": {},
        "msg": ""
    }
    :param fn:
    :return:
    """

    @wraps(fn)
    def _decorated(*args, **kwargs):
        try:
            return _api_standard_success_response(fn(*args, **kwargs))
        except SchemaError as ex:
            return _api_standard_failed_response("Error validating schema: \n error location: {} \n msg: {}".
                                                 format(" --> ".join([i for i in ex.path]), ex.message))
        except ValidationError as ex:
            return _api_standard_failed_response(
                "JSON data does not conform to schema regulations: \n error field: {}\n prompt msg:{}".
                format(" --> ".join([str(i) for i in ex.path]), ex.message))
        except Exception as ex:
            return _api_standard_failed_response(msg=ex.msg, code=ex.code)
        except BaseException as ex:
            raise ex

    return _decorated


def _api_standard_success_response(data):
    return _api_standard_response(code=0, data=data, msg=None)


def _api_standard_failed_response(msg, code=500):
    return _api_standard_response(code=code, data=None, msg=msg)


def _api_standard_response(code, data, msg):
    response = {
        "code": code,
        "data": data,
        "msg": msg
    }
    return flask.jsonify(response)



class Load(Resource):
    @staticmethod
    @api_response_handler
    def post():
        """
            ---
            tags:
              - Load
            parameters:
              - name: config_path
                in: body
                required: true
                schema:
                  properties:
                    message:
                      type: string
                      example: '/usr/bin/xx/config.yaml'

            definitions:
              Response:
                required:
                properties:
                  code:
                    type: integer
                    example: 0
                  msg:
                    type: string
                    description: 错误信息
                    example: test failed.
                  data:
                    type: object
            responses:
              200:
                description: response template
                schema:
                  $ref: '#/definitions/Response'
            """
        my_schema = {
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string"
                        }
                    }
                }
        body = request.json
        validate(instance=body, schema=my_schema)
        response = "Load"
        return response


class Get(Resource):
    @staticmethod
    @api_response_handler
    def post():
        """
            ---
            tags:
              - Get
            parameters:
              - name: key
                in: body
                required: true
                schema:
                  properties:
                    message:
                      type: string
                      example: 'pkgs.gcc.version'

            definitions:
              Response:
                required:
                properties:
                  code:
                    type: integer
                    example: 0
                  msg:
                    type: string
                    description: 错误信息
                    example: test failed.
                  data:
                    type: object
            responses:
              200:
                description: response template
                schema:
                  $ref: '#/definitions/Response'
            """
        my_schema = {
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string"
                        }
                    }
                }
        body = request.json
        validate(instance=body, schema=my_schema)

        response = "Get"
        return response

class Out(Resource):
    @staticmethod
    @api_response_handler
    def post():
        """
            ---
            tags:
              - Out
            parameters:
              - name: packages
                in: body
                required: true
                schema:
                  properties:
                    message:
                      type: string
                      example: 'pkgs.gcc'

            definitions:
              Response:
                required:
                properties:
                  code:
                    type: integer
                    example: 0
                  msg:
                    type: string
                    description: 错误信息
                    example: test failed.
                  data:
                    type: object
            responses:
              200:
                description: response template
                schema:
                  $ref: '#/definitions/Response'
            """
        my_schema = {
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string"
                        }
                    }
                }
        body = request.json
        validate(instance=body, schema=my_schema)

        response = "Out"
        return response