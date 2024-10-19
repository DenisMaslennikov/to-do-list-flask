"""WSGI runner."""

import os
import sys

sys.path.append(os.path.dirname(__file__))

from app import get_app
from config import ProductionConfig

flask_app = get_app(ProductionConfig)


def application(environ, start_response):
    """WSGI application."""
    return flask_app(environ, start_response)
