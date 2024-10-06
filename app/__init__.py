from flask import Flask

from app.api import api


def get_app(config) -> Flask:
    """
    Get flask application.

    :param config:
    """
    app = Flask(__name__)
    app.config.from_object(config)

    api.init_app(app)
    return app
