# -*- coding: utf-8 -*-
from chalice import Chalice

app = Chalice(app_name="macumba_pass")


@app.route('/')
def index():
    return {'message': 'Hello World'}
