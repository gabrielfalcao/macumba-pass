# -*- coding: utf-8 -*-
import botocore.exceptions
import logging

from . import awsgi
from .handlers import app

logger = logging.getLogger('macumba_pass.error')


def application(event, context):
    try:
        return awsgi.response(app, event, context)
    except botocore.exceptions.ProfileNotFound as e:
        logger.exception({'message': 'failed to handle event', 'event': repr(event)})
        raise RuntimeError(e)


__all__ = ('application', )
