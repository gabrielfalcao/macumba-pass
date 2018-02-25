# -*- coding: utf-8 -*-
import json
from decimal import Decimal


def aws_response(body=None, headers=None, status=200):
    """generates a valid AWS lambda HTTP response
    :param body: any non-string object will be json-serialized
    :param headers: a dictionary or iterable of key/value tuple-pairs
    :param status: the HTTP status code
    :returns: a valid lambda function response dictionary with the keys: ``body``, ``headers``, ``statusCode``
    """
    # TODO: support CORS
    # ------------------
    # "Access-Control-Allow-Origin": "*",
    # "Access-Control-Allow-Credentials": True

    response = {
        'headers': {
            'Content-Type': 'application/json',
        }
    }
    if not isinstance(body, str):
        body = json_serialize(body)

    response['body'] = body
    response['headers'].update(headers or tuple())
    response['statusCode'] = status
    return response


class DecimalEncoder(json.JSONEncoder):
    # This is a workaround for: http://bugs.python.org/issue16535
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(str(obj))

        return super(DecimalEncoder, self).default(obj)


def json_serialize(*args, **kw):
    kw['cls'] = DecimalEncoder
    return json.dumps(*args, **kw)


def json_deserialize(*args, **kw):
    kw['parse_float'] = Decimal
    return json.loads(*args, **kw)
