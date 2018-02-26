# -*- coding: utf-8 -*-
from .application import app
from .storage import *  # noqa


@app.route('/')
def index():
    params = app.current_request.query_params
    msg = params.get('message', 'Hello World')
    return {'message': msg}
