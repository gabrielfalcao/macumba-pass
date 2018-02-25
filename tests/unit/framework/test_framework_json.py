# -*- coding: utf-8 -*-
from decimal import Decimal
from macumba_pass.web.framework import json_serialize
from macumba_pass.web.framework import json_deserialize


def test_json_serialize():
    "web.framework.json_serialize() should return decode Decimal into string"

    result = json_serialize({'value': Decimal('3.14'), 'label': 'pi'})
    result.should.equal('{"value": 3.14, "label": "pi"}')


def test_json_deserialize():
    "web.framework.json_deserialize() should return decode Decimal into string"

    result = json_deserialize('{"value": 3.14, "label": "pi"}')
    result.should.equal({'value': Decimal('3.14'), 'label': 'pi'})
