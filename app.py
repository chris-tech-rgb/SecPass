from datetime import datetime

from flask import Flask
from flask import request
from flask_cors import CORS
import json
import psycopg2
import uuid

def connect(con, curs):
    con = psycopg2.connect(
        database="SecPass",
        host="127.0.0.1",
        user="postgres",
        password="114514",
        port="5432"
    )
    curs = conn.cursor()


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

conn = psycopg2.connect(
    database="SecPass",
    host="127.0.0.1",
    user="postgres",
    password="114514",
    port="5432"
)
cursor = conn.cursor()


@app.route('/user/login', methods=['POST'])
def user_login():
    request_form = request.get_json()
    username = request_form['username']
    password = request_form['password']
    cursor.execute("SELECT _password_ FROM userlist WHERE _username_='" + username + "'")
    user_password = cursor.fetchone()
    if user_password is not None and password == user_password[0]:
        token = json.dumps({
            'token': str(uuid.uuid4())
        })
        response_form = json.dumps({
            'code': 20000,
            'data': token
        })
        return response_form
    else:
        response_form = json.dumps({
            'code': 60204,
            'message': '用户名或密码不正确'
        })
        return response_form


@app.route('/user/info')
def user_info():
    info = json.dumps({
        'roles': ['user'],
        'introduction': 'none',
        'avatar': 'none',
        'name': 'none'
    })
    response_form = json.dumps({
        'code': 20000,
        'data': info
    })
    return response_form


@app.route('/user/logout', methods=['POST'])
def user_logout():
    return json.dumps({
        'code': 20000,
        'data': 'success'
    })


@app.route('/table/list')
def table_list():
    cursor.execute("SELECT * FROM password")
    password_list = cursor.fetchall()
    total = len(password_list)
    items = []
    for i in password_list:
        item = dict.fromkeys(['uuid', 'website', 'username', 'password', 'last_update', 'safety'])
        item['uuid'] = i[0]
        item['website'] = i[2]
        item['username'] = i[3]
        item['password'] = i[4]
        item['last_update'] = i[5]
        item['safety'] = i[6]
        items.append(item)
    response_form = json.dumps({
        'code': 20000,
        'data': {
            'items': items,
            'total': total
        }
    })
    return response_form


@app.route('/form/submit', methods=['POST'])
def form_submit():
    request_form = request.get_json()
    user = request_form['user']
    website = request_form['website']
    username = request_form['username']
    password = request_form['password']
    safety = request_form['safety']
    cursor.execute("SELECT _uid_ FROM userlist WHERE _username_='" + user + "'")
    user_id = cursor.fetchone()[0]
    _uuid = str(uuid.uuid4())
    last_update = str(datetime.now().date())
    cursor.execute("INSERT INTO password VALUES ('" + _uuid + "', '" + user_id + "', '" + website + "', '" +
                   username + "', '" + password + "', '" + last_update + "', '" + safety + "')")
    conn.commit()
    conn.closed()
    connect(conn, cursor)
    return json.dumps({
        'code': 20000
    })


@app.route('/form/update', methods=['POST'])
def form_update():
    request_form = request.get_json()
    _uuid = request_form['uuid']
    website = request_form['website']
    username = request_form['username']
    password = request_form['password']
    safety = request_form['safety']
    last_update = str(datetime.now().date())
    cursor.execute("UPDATE password SET _website_='" + website + "', _username_='" +
                   username + "', _password_='" + password + "', _last_update_='" +
                   last_update + "', _safety_='" + safety + "' WHERE _uuid_='" + _uuid + "'")
    conn.commit()
    conn.closed()
    connect(conn, cursor)
    return json.dumps({
        'code': 20000
    })


@app.route('/form/delete', methods=['POST'])
def form_delete():
    request_form = request.get_json()
    _uuid = request_form['uuid']
    cursor.execute("DELETE FROM password WHERE _uuid_='" + _uuid + "'")
    conn.commit()
    return json.dumps({
        'code': 20000
    })


# Server
# app.run(host='172.25.113.153')
app.run(host='192.168.206.128')
