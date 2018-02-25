# -*- coding: utf-8 -*-
from chalice import Chalice
from chalice import Response

from .testing import ChaliceTestClient
from .serializers import json


class Application(Chalice):
    def test_client(self):
        return ChaliceTestClient(self)


def json_response(data, status_code=200, headers=None):
    headers = headers or {}
    headers['Content-Type'] = 'application/json'
    return Response(json.dumps(data), headers=headers, status_code=status_code)
