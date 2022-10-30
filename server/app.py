from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz
from flask_cors import CORS
from psycopg2.errors import NumericValueOutOfRange

engine = db.create_engine(
    "postgresql+psycopg2://postgres:P@ssw0rd@127.0.0.1:5432/postgres")
# engine = db.create_engine(
#   "postgresql+psycopg2://rbadmin_app2:postgres@10.187.232.28:5432/landing")

SQLALCHEMY_ENGINE_OPTIONS = {
    # 'pool': QueuePool(creator),
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': True
}

connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

metadata = db.MetaData()
feedback = db.Table('feedback', metadata, autoload=True, autoload_with=engine)
requirement = db.Table('requirement', metadata,
                       autoload=True, autoload_with=engine)
subscribe = db.Table('subscribe', metadata,
                     autoload=True, autoload_with=engine)
contact = db.Table('contact', metadata, autoload=True,
                   autoload_with=engine)

engine.dispose()

# 设置CORS跨域


def register_cors(app):
    CORS(app, supports_credentials=True)


def create_app():
    # 实例化flask
    app = Flask(__name__)
    # 一系列初始化
    register_cors(app)
    return app


app = create_app()


def render_results(results, table):
    context = []
    for result in results:
        # Convert unix time to readable time
        tz = pytz.timezone('Asia/Shanghai')
        timestamp = datetime.fromtimestamp(result[1], pytz.timezone('Asia/Shanghai'))
        create_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        dict = {}
        if table == feedback:
            dict = {'id': result[0],
                    'create time': create_str,
                    'star': result[4],
                    'comment': result[5],
                    'email': result[6]}
        elif table == requirement:
            dict = {'id': result[0],
                    'create time': create_str,
                    'email': result[4],
                    'comment': result[5]}
        elif table == subscribe:
            dict = {'id': result[0],
                    'create time': create_str,
                    'email': result[4]}
        elif table == contact:
            dict = {'id': result[0],
                    'create time': create_str,
                    'email': result[4],
                    'goal': result[5],
                    'help': result[6],
                    'number': result[7],
                    'individual': result[8]}

        context.append(dict)

    return jsonify(context)


def filter(results, data, table):
    try:
        # reinitialize the searching query
        results = session.query(table).order_by(table.c.create_time.desc())

        if bool(data.get('has_date')):
            start = data.get('start_time')
            end = data.get('end_time')
            results = results.filter(table.c.create_time.between(start, end))

        if bool(data.get('has_query')):
            tag = int(data.get('tag'))
            key = data.get('key')
            if tag == 1:
                results = results.filter_by(id=key)
            elif tag == 2:
                try:
                    results = results.filter_by(star=key)
                except NumericValueOutOfRange as e:
                    results.rollback()
            elif tag == 3:
                if table == feedback:
                    results = results.filter_by(comment=key)
                else:
                    results = results.filter_by(requirement=key)
            elif tag == 4:
                results = results.filter_by(email=key)
            else:
                print('Invalid tag')
                results = results.filter_by(id='-1')
    except Exception as e:
        print('filter')
    return results


@app.route('/', methods=['GET', 'POST'])
def get_requirement():
    ROW_LIMIT = 10  # Predefined row limit for each page

    data = request.get_json()
    print(data)

    table = feedback
    results = None
    if data is not None:
        if data.get('active_name') == 'second':
            table = requirement
        elif data.get('active_name') == 'third':
            table = subscribe
        elif data.get('active_name') == 'fourth':
            table = contact

        results = session.query(table).order_by(table.c.create_time.desc())
        if data.get('command') == 'filter':
            results = filter(results, data, table)
        # elif data.get('command') == 'filter-pagination':
        #     print('pagination HHHHHHHHHHHHHHHHHHHHHHHH')
        #     results = result_storage
        #     offset = (data.get('current_page') - 1) * data.get('page_size')
        #     results = results.limit(ROW_LIMIT).offset(offset)
        else:
            offset = (data.get('current_page') - 1) * data.get('page_size')
            results = results.limit(ROW_LIMIT).offset(offset)
    else:
        results = session.query(table).order_by(table.c.create_time.desc())
        results = results.limit(ROW_LIMIT).offset(0)

    return render_results(results, table)


if __name__ == '__main__':
    app.run(debug=True)
