import os
import logging

from flask import Flask

from app.routes.api_route import api_route
from app.view import bp


def create_app() -> Flask:
    logging.getLogger(__name__)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
    )

    app.register_blueprint(bp)
    app.register_blueprint(api_route)

    return app
