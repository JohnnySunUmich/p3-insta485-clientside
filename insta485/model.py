"""Insta485 model (database) API."""
import sqlite3
from sqlite3 import Connection, Cursor
from flask import g
from insta485 import app


def dict_factory(cursor: Cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    {'username': 'awdeorio', 'fullname': 'Andrew DeOrio',
    'email': 'awdeorio@umich.edu', 'filename': 'pfp.jpg',
    'password': 'sha512', 'created': '2023-01-13 06:32:26'}
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db() -> Connection:
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in g:
        g.conn: Connection = sqlite3.connect(
            str(app.config['DATABASE_FILENAME']))
        g.conn.row_factory = dict_factory
        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        g.conn.cursor().execute("PRAGMA foreign_keys = ON")
    return g.conn


@app.teardown_appcontext
def close_db(error) -> None:
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    conn: Connection = g.pop('sqlite_db', None)
    if conn is not None:
        conn.commit()
        conn.close()
