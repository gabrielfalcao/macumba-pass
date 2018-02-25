# -*- coding: utf-8 -*-
import sys
import logging
from nicelog.formatters import Colorful


def create_log_handler():
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(Colorful())
    handler.setLevel(logging.DEBUG)
    return handler
