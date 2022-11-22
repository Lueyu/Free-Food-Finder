from flask import Flask, jsonify, session, make_response, request, g
from flask_cors import CORS
from flask_session import Session
import sqlite3
import flask
import pathlib
import datetime
import json
import os


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def get_db():
    """Open a new database connection.
    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in g:
        db_filename = './var/icu_diary.sqlite3'
        g.sqlite_db = sqlite3.connect(db_filename)
        g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.
    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    db_cur = g.pop('db_cur', None)
    db_con = g.pop('db_con', None)
    if db_con is not None:
        db_con.commit()
        db_cur.close()
        db_con.close()


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


@app.route('/', methods=['GET', 'POST'])
def index_page():
    data = request.get_json()
    print(data)
    return jsonify('main')


if __name__ == '__main__':
    app.run(debug=True)
