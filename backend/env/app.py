from flask import Flask, jsonify, session, make_response, request, g
from flask_cors import CORS, cross_origin
import sqlite3
import flask
import pathlib
import datetime
from datetime import timezone
import dateutil.parser
import json
import os


# configuration
DEBUG = True

# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def get_db():
    """Open a new database connection.
    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in g:
        db_filename = './sql/var/foodDB.sqlite3'
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


@app.route('/', methods=['POST'])
@cross_origin()
def index_page():
    data = request.get_json()
    connection = get_db()

    loc_name = data['location']["formatted_address"]
    lat = data['location']['geometry']['location']['lat']
    lng = data['location']['geometry']['location']['lng']

    dateobj1 = dateutil.parser.isoparse(data['date1'])
    dateobj1 = dateobj1.replace(tzinfo=timezone.utc).astimezone(
        tz=dateutil.tz.gettz('US/Eastern'))
    dateobj2 = dateutil.parser.isoparse(data['date2'])
    dateobj2 = dateobj2.replace(tzinfo=timezone.utc).astimezone(
        tz=dateutil.tz.gettz('US/Eastern'))

    month = dateobj1.strftime("%m")
    day = dateobj1.strftime("%d")
    time = dateobj2.strftime("%H:%M")
    date_val = month+'/'+day+' '+time
    connection.execute(
        "INSERT INTO info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (None, data['name'], data['campus'], loc_name, lat, lng,
         data['type'], date_val, data['req'], data['event']))
    connection.commit()
    return jsonify('Post success')


@app.route('/query', methods=['GET', 'POST'])
@cross_origin()
def index_page_query():
    query = request.get_json()
    location = query['location']
    foodType = query['type']
    connection = get_db()
    info = connection.execute(
        "SELECT campus,locName,lat,lng,foodType,foodDate,requirement,organization FROM info"
    )
    if location is not "":
        location = '%'+location+'%'
        info.execute("SELECT * FROM info WHERE locName LIKE ?", (location, ))
    if foodType is not "":
        foodType = '%'+foodType+'%'
        info.execute("SELECT * FROM info WHERE foodType LIKE ?", (foodType, ))
    res = []
    for row in info:
        res.append(
            {
                "campus": row["campus"],
                "location": row["locName"],
                "lat": row["lat"],
                "lng": row["lng"],
                "type": row["foodType"],
                "time": row["foodDate"],
                "req": row["requirement"],
                "org": row["organization"]
            }
        )
    # print(res)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
