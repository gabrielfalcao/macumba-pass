# -*- coding: utf-8 -*-

import sys
import logging
import watchtower


def create_log_handler(formatter=None):
    if sys.platform == 'darwin':
        handler = logging.StreamHandler(sys.stderr)
    else:
        watchtower.CloudWatchLogHandler()

    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    return handler
