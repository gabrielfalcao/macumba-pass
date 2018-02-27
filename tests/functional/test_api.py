# -*- coding: utf-8 -*-
from macumba_pass.web.framework.serializers import json
from .scenarios import with_localstack


@with_localstack('s3')
def test_create_password(context):
    ("POST /api/v1/secret should create an s3 bucket if not exists")

    pwdata = {
        'label': 'personal/gmail account',
        'password': 'this is very secret',
    }
    response = context.http.post('/api/v1/secret', body=pwdata)

    response.status_code.should.equal(200)
    response.headers.should.equal({
        'Content-Type': 'application/json',
    })
    data = json.loads(response.body)
    data.should.equal({
        'label': 'personal/gmail-account',
        'value': {
            'password': 'this is very secret',
        }
    })
