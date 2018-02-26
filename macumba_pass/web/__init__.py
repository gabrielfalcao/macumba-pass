# -*- coding: utf-8 -*-
import awsgi
import botocore.exceptions

from .handlers import app


def application(event, context):
    try:
        return awsgi.response(app, event, context)
    except botocore.exceptions.ProfileNotFound as e:
        app.logger.exception({'message': 'failed to handle event', 'event': dict(event)})
        raise RuntimeError(e)


__all__ = ('application', )
