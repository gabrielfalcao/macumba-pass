# -*- coding: utf-8 -*-
from .base import app

from macumba_pass.web.framework import json_response
from macumba_pass.web.helpers import PasswordKeyStore


@app.route('/api/v1/password', methods=['POST'])
def set_password():
    store = PasswordKeyStore()
    bucket = store.get_bucket()
    response = {
        'bucket_name': bucket['Name']
    }
    return json_response(response)


@app.route('/api/v1/password/{label}', methods=['GET'])
def retrieve_password(label):
    store = PasswordKeyStore()
    bucket = store.get_bucket()
    response = {
        'bucket_name': bucket['Name']
    }
    return json_response(response)
