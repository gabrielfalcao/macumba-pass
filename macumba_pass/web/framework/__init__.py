# -*- coding: utf-8 -*-
import logging
from flask import Flask
from flask import Response

from .serializers import json
from .logs import create_log_handler


class Application(Flask):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        handler = create_log_handler()
        level = logging.DEBUG
        for name in [None, 'boto', 'werkzeug', 'flask', 'macumba_pass']:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.addHandler(handler)

        self.logger.addHandler(handler)
        self.logger.setLevel(level)

    # def test_client(self):
    #     return ChaliceTestClient(self)


def json_response(data, status=200, headers=None, cors_origin=None):
    headers = headers or {}
    headers['Content-Type'] = 'application/json'
    if cors_origin is not None:
        headers.update({
            "Access-Control-Allow-Origin": cors_origin,
            "Access-Control-Allow-Credentials": 'true'
        })

    return Response(json.dumps(data), headers=headers, status=status)
