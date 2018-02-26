# -*- coding: utf-8 -*-

import logging
import watchtower


def create_log_handler(formatter=None):
    handler = watchtower.CloudWatchLogHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    return handler
