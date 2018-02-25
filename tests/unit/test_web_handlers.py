# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from macumba_pass.web.api_handlers import index


def test_index_api_handler():
    "web.api_handlers.index should return hello world"

    event = {}
    context = {}
    response = index(event, context)

    response.should.equal({
        'body': '{"message": "Hello World"}',
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200,
    })
