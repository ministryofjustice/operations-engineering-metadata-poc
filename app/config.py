import os
from types import SimpleNamespace

config = SimpleNamespace(
    database=SimpleNamespace(
        endpoint=os.environ.get('DATABASE_ENDPOINT') or 'localhost:5432',
        user=os.environ.get('DATABASE_USERNAME') or 'postgres',
        password=os.environ.get('DATABASE_PASSWORD') or 'postgres',
        name=os.environ.get('DATABASE_NAME') or 'postgres'
    )
)
