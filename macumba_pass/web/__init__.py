# -*- coding: utf-8 -*-
import awsgi
from .handlers import app


def application(event, context):
    return awsgi.response(app, event, context)


__all__ = ('application', )
