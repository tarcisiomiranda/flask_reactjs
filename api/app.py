from datetime import datetime, timedelta, date
from flask_apscheduler import APScheduler
from flask.globals import request
from mysql_addon import MySQLAddOn
from crypt import methods
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import json
import time
import sys
import re

class ConfigScheduler:
    SCHEDULER_API_ENABLED = True

''' Start Flask and Scheduler '''
app = Flask(__name__)
CORS(app)
scheduler = APScheduler()

def filter_escolha(lista_original):
    filtered = []
    _pattern = r'(\d{1,2})(.*)'

    for linha in lista_original:
        if re.match(_pattern, linha):
            res = re.split(_pattern, linha)
            res_clear = [item.strip() for item in res if item.strip()]
            print('LIMPOS -> ', 'Total: ', len(res_clear), 'Separados: ', res_clear)

            if len(res_clear) == 2:
                filtered.append({res_clear[0] : res_clear[1]})

    return filtered

@app.route('/api/escolha', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_escolhidos():
    if request.method == 'POST':
        data = request.json
        print('ESCOLHA POST ', data)

        jogadores = []
        for d in data['names'].splitlines():
            jogadores.append(d)

        filtrado = filter_escolha(jogadores)
        print('| == filtrado ==> ', filtrado)

        return jsonify({'message': filtrado})
    else:
        return jsonify({'message': 'Nao foi post'})

# API Rest
@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_users():
    try:
        if request.method == 'POST':
            data = request.json
            print('POST > ', data)
            if not all(key in data for key in ['name', 'email', 'mobile', 'birth_date']):
                return jsonify({'message': 'JSON inválido'}), 400

            # TODO
            my_sql = MySQLAddOn()
            my_sql.conn.autocommit = True
            cursor = my_sql.conn.cursor(dictionary=True)

            query = "INSERT INTO users (name, email, mobile, birth_date) VALUES (%s, %s, %s, %s)"
            values = (data['name'], data['email'], data['mobile'], data['birth_date'])

            cursor.execute(query, values)

            return jsonify({'message': 'User created successfully'}), 201

        elif request.method == 'PUT':
            # TODO
            my_sql = MySQLAddOn()
            my_sql.conn.autocommit = True
            cursor = my_sql.conn.cursor(dictionary=True)

            data = request.json
            print('PUT > ', data)

            query = "UPDATE users SET name = %s, email = %s, mobile = %s, birth_date = %s WHERE id = %s"
            values = (data['name'], data['email'], data['mobile'], data['birth_date'], data['id'])

            # TODO - Validar update
            cursor.execute(query, values)
            return jsonify({'message': 'User updated successfully'}), 201

        elif request.method == 'DELETE':
            # TODO
            my_sql = MySQLAddOn()
            my_sql.conn.autocommit = True
            cursor = my_sql.conn.cursor(dictionary=True)

            data = request.get_json()
            print('DELETE > ', data)

            # TODO - Validar delte
            delete_query = "DELETE FROM users WHERE id = %s"
            cursor.execute(delete_query, (int(data['id']),))

            return jsonify({'message': 'User deleted successfully'}), 201

        elif request.method == 'GET':
            # TODO
            my_sql = MySQLAddOn()
            my_sql.conn.autocommit = True
            cursor = my_sql.conn.cursor(dictionary=True)

            users = 'SELECT * FROM users'
            cursor.execute(users)
            res = cursor.fetchall()

            return jsonify(res)

        else:
            return jsonify({'message': 'no method send'}), 201

    except Exception as e:
        return jsonify('error: {}'.format(e))
    
    # finally:
        # cursor.close()
        # conn.close()


# start flask
if __name__ == '__main__':
    # Scheduler
    # app.config.from_object(ConfigScheduler())
    scheduler.init_app(app)
    scheduler.start()
    # Flask
    app.run(debug=True, host='0.0.0.0', port=8800, use_reloader=True)
