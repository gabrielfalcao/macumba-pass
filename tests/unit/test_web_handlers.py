# -*- coding: utf-8 -*-
from mock import patch
from macumba_pass.web.handlers import index
from macumba_pass.web.handlers.storage import set_password


@patch('macumba_pass.web.handlers.app')
def test_index_api_handler(app):
    "web.handlers.index should return hello world"
    app.current_request.query_params = {
        'message': 'Cool',
    }
    response = index()

    response.should.equal({
        "message": "Cool"
    })


@patch('macumba_pass.web.handlers.storage.app')
@patch('macumba_pass.web.handlers.storage.json_response')
@patch('macumba_pass.web.handlers.storage.PasswordKeyStore')
def test_set_password(PasswordKeyStore, json_response, app):
    "web.handlers.storage.set_password() should create bucket"
    store = PasswordKeyStore.return_value
    store.get_bucket.return_value = {
        'Name': 'macumba-secrets'
    }

    response = set_password()

    response.should.equal(json_response.return_value)

    json_response.assert_called_once_with({
        "bucket_name": "macumba-secrets"
    })

    store.get_bucket.assert_called_once_with()
