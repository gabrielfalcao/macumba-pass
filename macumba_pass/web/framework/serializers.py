# -*- coding: utf-8 -*-
from json import JSONEncoder
from json import dumps as json_dumps
from json import loads as json_loads
from decimal import Decimal


class DecimalEncoder(JSONEncoder):
    # This is a workaround for: http://bugs.python.org/issue16535
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(str(obj))

        return super(DecimalEncoder, self).default(obj)


def json_serialize(*args, **kw):
    if 'cls' not in kw:
        kw['cls'] = DecimalEncoder

    return json_dumps(*args, **kw)


def json_deserialize(*args, **kw):
    kw['parse_float'] = Decimal
    return json_loads(*args, **kw)


class json(object):
    @staticmethod
    def dumps(*args, **kw):
        return json_serialize(*args, **kw)

    @staticmethod
    def loads(*args, **kw):
        return json_deserialize(*args, **kw)
