# -*- coding: utf-8 -*-
from macumba_pass.web.framework import json_response

from .application import app


@app.errorhandler(500)
def handle_500():
    msg = 'internal server error'
    app.logger.exception(msg)
    return json_response({
        'error': msg,
    }, status=500)
