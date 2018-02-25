# -*- coding: utf-8 -*-
from chalice.config import Config
from chalice.local import LocalGateway
from chalice import Response

from .logs import create_log_handler
from .serializers import json_serialize


class ChaliceTestClient(object):
    def __init__(self, app_object, config=None):
        self.application = app_object
        self.config = config or Config()
        # self.application._debug = True
        self.server = LocalGateway(self.application, self.config)

        self.log_handler = create_log_handler()
        self.application.debug = True
        self.application.log.addHandler(self.log_handler)

    def request(self, path, body=None, headers=(), method='GET', json=False):
        headers = dict(headers or {})
        if not isinstance(body, str):
            json = True

        if json:
            headers['Content-Type'] = 'application/json'
            body = json_serialize(body)

        response = dict(self.server.handle_request(
            method=method.upper(),
            path=path,
            headers=headers,
            body=body,
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
