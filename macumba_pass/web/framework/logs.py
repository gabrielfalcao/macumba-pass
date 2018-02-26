# -*- coding: utf-8 -*-
import sys
import logging


def create_log_handler(formatter=None):
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    return handler
