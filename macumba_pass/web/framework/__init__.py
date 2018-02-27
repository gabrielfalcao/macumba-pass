# -*- coding: utf-8 -*-
import logging
from chalice import Chalice
from chalice import Response
from .testing import ChaliceTestClient
from .serializers import json
from .logs import create_log_handler


class Application(Chalice):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        handler = create_log_handler()

        level = logging.INFO
        for name in [None, 'boto', 'werkzeug', 'flask', 'macumba_pass', 'macumba_pass.error']:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.addHandler(handler)

        self.log.addHandler(handler)
        self.log.setLevel(level)

    def test_client(self):
        return ChaliceTestClient(self)


def json_response(data, status_code=200, headers=None, cors_origin=None):
    headers = headers or {}
    headers['Content-Type'] = 'application/json'
    if cors_origin is not None:
        headers.update({
            "Access-Control-Allow-Origin": cors_origin,
            "Access-Control-Allow-Credentials": 'true'
        })

    return Response(json.dumps(data), headers=headers, status_code=status_code)
