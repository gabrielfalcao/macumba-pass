# -*- coding: utf-8 -*-
from .base import app

from macumba_pass.web.framework import json_response
from macumba_pass.web.helpers import PasswordKeyStore


@app.route('/api/v1/password', methods=['POST'])
def set_password_v1():
    store = PasswordKeyStore()
    bucket = store.get_or_create_bucket('macumba-secrets')
    response = {
        'bucket_name': bucket['Name']
    }
    return json_response(response)


@app.route('/api/v1/password/{label}', methods=['GET'])
def retrieve_password_v1(label):
    store = PasswordKeyStore()
    bucket = store.get_or_create_bucket('macumba-secrets')
    response = {
        'bucket_name': bucket['Name']
    }
    return json_response(response)
