# -*- coding: utf-8 -*-

from macumba_pass.web.framework import aws_response


def test_aws_response_simple():
    "framework.aws_response() should return an AWS response"

    response = aws_response({'message': 'Hello World'})

    response.should.equal({
        'body': '{"message": "Hello World"}',
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': 200,
    })
