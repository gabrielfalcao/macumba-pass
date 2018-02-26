# -*- coding: utf-8 -*-
from flask import request
from .application import app
from .storage import *  # noqa


@app.route('/')
def index():
    msg = request.values.get('message', 'Hello World')
    return {'message': msg}
