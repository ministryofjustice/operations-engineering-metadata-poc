import os

from app.db import DatabaseInterface
from flask import Blueprint

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    '''Entrypoint into the application'''
    db = DatabaseInterface(
        os.getenv("TABLE_NAME", "test_table")
    )

    all = db.get_all_items()

    return all
