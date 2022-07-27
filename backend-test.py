# backend-service for тестового задание на должность frontend-dev junior
# Написано на коленке за 15 минут (код соответствующий)
# Stanislav Rychkov (TG: rs_root)
# Media-land | sshvps.ru | 2022

from flask import Flask, request
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)

TOKEN_API = 'KLJ3fedchbjn*&DN+fdsbnmljhnkjh'


class DB:
    def __init__(self):
        self._id = 0

    @property
    def incr(self):
        self._id += 1
        return self._id


db = DB()

note_list = [{
    # Заметка тестовая
    'id': db.incr,
    'date_create': datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M:%S'),
    'title': '#Заметка_1',
    'body': 'Тут какой то текст заметки, бла бла бла...',
    'color': '#F00000',
}]


def token_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        token = request.headers.get('token', '')
        if token != TOKEN_API:
            return json.dumps({'error': 'Не авторизован'}), 401
        return func(*args, **kwargs)

    return wrap


@app.route('/', methods=['GET'])
def main():
    return rf'''<pre>
<p style="margin-block-end: unset;color: blue;font-size: 15;font-weight: 900;">
                 _ _         __                 _
  /\/\   ___  __| (_) __ _  / /  __ _ _ __   __| |
 /    \ / _ \/ _` | |/ _` |/ /  / _` |  _ \ / _` |
/ /\/\ \  __/ (_| | | (_| / /__| (_| | | | | (_| |
\/    \/\___|\__,_|_|\__,_\____/\__,_|_| |_|\__,_|
                                     Тестовое задание </p>
                                        
# backend-service for тестового задание на должность frontend-dev junior
# Написано на коленке за 15 минут (код соответствующий)
# Stanislav Rychkov (TG: rs_root)
# Media-land | sshvps.ru | 2022

<pre>
''', 200


@app.route('/login', methods=['POST'])
def login():
    try:
        data = json.loads(request.data)
    except Exception as Err:
        return json.dumps({'error': 'Не валидный Json'}), 501

    if not data.get('login', '') or not data.get('password', ''):
        return json.dumps({'error': 'не верный json',
                           'correct_data': {'login': 'test@test.test', 'password': 'U*HYGBhunjuHBJNKM'}}), 501

    if 'test@test.test' == data['login'] and 'U*HYGBhunjuHBJNKM' == data['password']:
        return json.dumps({'status': 'ok', 'token': TOKEN_API})

    return json.dumps({'error': 'Не верный логин или пароль'}), 401


@app.route('/note', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def note():
    try:
        data = json.loads(request.data)
    except Exception as Err:
        return json.dumps({'error': 'Не валидный Json'}), 501

    if request.method != 'GET':
        if not data.get('title', '') or not data.get('body', '') or not data.get('color', ''):
            return json.dumps({'error': 'не верный json',
                               'correct_data': {
                                   "id": 1,
                                   "title": "#Заметка_1",
                                   "body": "Тут какой то текст заметки, бла бла бла...",
                                   "color": "#F00000"
                               }}), 502

        if request.method in ['PUT', 'DEL']:
            if not data.get('id'):
                return json.dumps({'error': 'в JSON нет обязательного параметра id'}), 501

    if request.method == 'GET':
        return json.dumps({'status': 'ok', 'notes': note_list})

    if request.method == 'POST':
        note = {'id': db.incr,
                'date_create': datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M:%S'),
                'title': data['title'],
                'body': data['body'],
                'color': data['color']
                }
        note_list.append(note)
        return json.dumps({'status': 'ok', 'notes': note}), 202

    if request.method == 'PUT':
        ids_list = next((i for i, item in enumerate(note_list) if item["id"] == data['id']), None)

        if ids_list is None:
            return json.dumps({'error': 'нет такого id заметки в базе данных'}), 501

        note_list[ids_list] = {'id': data['id'],
                               'date_create': datetime.strftime(datetime.now(), '%m/%d/%Y %H:%M:%S'),
                               'title': data['title'],
                               'body': data['body'],
                               'color': data['color']}
        return json.dumps({'status': 'ok', 'notes': note_list[ids_list]}), 201

    if request.method == 'DELETE':
        ids_list = next((i for i, item in enumerate(note_list) if item["id"] == data['id']), None)

        if ids_list is None:
            return json.dumps({'error': 'нет такого id заметки в базе данных'}), 501

        del note_list[ids_list]
        return json.dumps({'status': 'ok'}), 204


if __name__ == '__main__':
    app.run()
