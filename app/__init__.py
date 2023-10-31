import logging

from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader
from flask_cors import CORS

from app.clients.db_client import DBClient
from app.routes.api_route import create_api_route
from app.routes.views import create_app_routes
from app.services.user_service import UserService

from app.views.errors import (page_not_found, server_forbidden,
                                   unknown_server_error, gateway_timeout)


def create_app(db_client: DBClient = None):
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s : %(message)s',
    )
    
    app = Flask(__name__, instance_relative_config=True)
    db_client = db_client or DBClient(app)
    user_service = UserService(db_client)
    app.register_blueprint(create_api_route(user_service))
    app.register_blueprint(create_app_routes(user_service))
    
    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}),
        ]
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    app.register_error_handler(403, server_forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, unknown_server_error)
    app.register_error_handler(504, gateway_timeout)

    # Security and Protection extenstions
    CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}})

    return app


