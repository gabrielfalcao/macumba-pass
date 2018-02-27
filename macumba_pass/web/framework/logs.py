# -*- coding: utf-8 -*-

import sys
import logging
import watchtower

logger = logging.getLogger('macumba_pass')


def create_log_handler(formatter=None):
    if sys.platform == 'darwin':
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = watchtower.CloudWatchLogHandler()

    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    return handler
