# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from macumba_pass.web.handlers import index


def test_index_api_handler():
    "web.handlers.index should return hello world"

    response = index()

    response.should.equal({
        "message": "Hello World"
    })
