# -*- coding: utf-8 -*-
from chalice.config import Config
from chalice.local import LocalGateway
from chalice import Response
from chalice.constants import DEFAULT_STAGE_NAME
from chalice.constants import DEFAULT_APIGATEWAY_STAGE_NAME
from datetime import datetime

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

        self.log_handler = create_log_handler()
        self.application.debug = True
        self.application.log.addHandler(self.log_handler)

    def request(self, path, body=None, headers=(), method='GET', authorization=None, json=False):
        headers = dict(headers or {})
        if not isinstance(body, str):
            json = True

        if json:
            headers['Content-Type'] = 'application/json'
            body = json_serialize(body)

        if not authorization and 'Authorization' not in headers:
            headers['Authorization'] = 'Credential=credential;Signature=signature;Date={}'.format(datetime.utcnow().isoformat())

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

    def get(self, path, headers=None):
        return self.request(path, headers=headers, method='get')

    def head(self, path, headers=None):
        return self.request(path, headers=headers, method='head')

    def post(self, path, body, headers=None):
        return self.request(path, body, headers=headers, method='post')

    def put(self, path, body, headers=None):
        return self.request(path, body, headers=headers, method='put')

    def patch(self, path, body, headers=None):
        return self.request(path, body, headers=headers, method='patch')

    def delete(self, path, body, headers=None):
        return self.request(path, body, headers=headers, method='delete')


def test_client(app):
    return ChaliceTestClient(app)
