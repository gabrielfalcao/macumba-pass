# -*- coding: utf-8 -*-
from .base import app

from macumba_pass.web.framework import json_response
from macumba_pass.web.helpers import PasswordKeyStore


def get_secret_metadata_from_request():
    body = app.current_request.json_body
    if not body:
        return {}

    label = body.pop('label')
    return label, body


def get_label_from_query_params():
    params = dict(app.current_request.query_params)
    return params.pop('label', None)


def json_bad_request(message):
    return json_response({'error': message}, status_code=400)


@app.route('/api/v1/secret', methods=['POST'])
def set_password():
    label, value = get_secret_metadata_from_request()

    if not label:
        return json_bad_request('missing label')

    if not value:
        return json_bad_request('missing secret data')

    store = PasswordKeyStore()
    secret_data = store.persist_secret(label, value)
    return json_response(secret_data)


@app.route('/api/v1/secret', methods=['GET'])
def retrieve_password():
    label = get_label_from_query_params()
    store = PasswordKeyStore()
    secret_data = store.retrieve_secret(label)
    return json_response(secret_data)
