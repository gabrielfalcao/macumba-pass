# -*- coding: utf-8 -*-
from mock import patch
from macumba_pass.web.handlers import index
from macumba_pass.web.handlers.storage import set_password


@patch('macumba_pass.web.handlers.request')
def test_index_api_handler(request):
    'web.handlers.index should return hello world'
    request.values = {
        'message': 'Cool',
    }
    response = index()

    response.should.equal({
        'message': 'Cool'
    })


@patch('macumba_pass.web.handlers.storage.request')
@patch('macumba_pass.web.handlers.storage.json_response')
@patch('macumba_pass.web.handlers.storage.PasswordKeyStore')
def test_set_password(PasswordKeyStore, json_response, request):
    'web.handlers.storage.set_password() should create bucket'
    request.get_json.return_value = {
        'label': 'twitter-password',
        'password': 'super secret',

    }
    store = PasswordKeyStore.return_value
    store.persist_secret.side_effect = lambda label, value: {
        'label': label,
        'value': value,
    }

    response = set_password()

    response.should.equal(json_response.return_value)

    json_response.assert_called_once_with({
        'label': 'twitter-password',
        'value': {
            'password': 'super secret',
        }
    })

    store.persist_secret.assert_called_once_with(
        'twitter-password',
        {'password': 'super secret', },
    )
