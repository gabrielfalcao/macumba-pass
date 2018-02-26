# -*- coding: utf-8 -*-
from .application import app
from flask import request
from macumba_pass.web.framework import json_response
from macumba_pass.web.helpers import PasswordKeyStore


def get_secret_metadata_from_request():
    data = request.get_json(silent=True) or dict(request.values)
    label = data.pop('label', None)
    return label, data


def json_bad_request(message):
    return json_response({'error': message}, status=400)


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
    label = request.values.get('label', None)
    store = PasswordKeyStore()
    secret_data = store.retrieve_secret(label)
    return json_response(secret_data)
