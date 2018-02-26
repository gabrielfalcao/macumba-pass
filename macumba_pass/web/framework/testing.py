# -*- coding: utf-8 -*-

from chalice.config import Config
from chalice.local import LocalGateway
from chalice import Response
from chalice.constants import DEFAULT_STAGE_NAME
from chalice.constants import DEFAULT_APIGATEWAY_STAGE_NAME
from datetime import datetime
from nicelog.formatters import Colorful


from .logs import create_log_handler
from .serializers import json_serialize


def create_test_config(application):
    default_params = {
        'project_dir': application.app_name,
        'api_gateway_stage': DEFAULT_APIGATEWAY_STAGE_NAME,
        'autogen_policy': True
    }
    params = {
        'default_params': default_params,
        'chalice_stage': DEFAULT_STAGE_NAME,
    }

    return Config(**params)


class ChaliceTestClient(object):
    def __init__(self, application, config=None):
        self.application = application
        self.config = config or create_test_config(application)
        # self.application._debug = True
        self.server = LocalGateway(self.application, self.config)

        self.log_handler = create_log_handler(Colorful())
        self.application.debug = True
        self.application.log.addHandler(self.log_handler)

    def request(self, path, body=None, headers=(), method='GET', json=False):
        headers = dict(headers or {})
        if not isinstance(body, str):
            json = True

        if json:
            headers['Content-Type'] = 'application/json'
            if body is not None:
                body = json_serialize(body)

        params = dict(
            method=method.upper(),
            path=path,
            headers=headers,
            body=body,
        )

        try:
            self.server.event_converter.create_lambda_event(**params)
        except ValueError as e:
            raise AssertionError(e)

        response = dict(self.server.handle_request(
            **params
        ))

        response['status_code'] = response.pop('statusCode')
        return Response(**response)

    def __getattr__(self, attr):
        if attr.upper() in ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'):
            return lambda *args, **kw: self.request(method=attr.lower(), *args, **kw)

        return object.__getattribute__(self, attr)


def test_client(app):
    return ChaliceTestClient(app)
