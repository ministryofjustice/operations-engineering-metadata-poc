from app.db import DatabaseInterface
from flask import Blueprint

bp = Blueprint("main", __name__)


@bp.route("/home")
def index():
    '''Entrypoint into the application'''
    return DatabaseInterface(table_name="cp-82071a5dad979a47").get_all_items()
