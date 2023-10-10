import os
import logging

from flask import Flask

from app.view import bp

logger = logging.getLogger(__name__)

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
)

app.register_blueprint(bp)
