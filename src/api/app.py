from datetime import datetime, timedelta, date
from flask_apscheduler import APScheduler
from flask.globals import request
from mysql_addon import MySQLAddOn
from crypt import methods
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import random
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

def filter_escolha(lista_original, number=1):
    filtered = []
    _pattern = r'(\d{1,2})(.*)'

    if len(lista_original) < 10:
        return {'message': ['Mínimo de 10 pessoas...']}

    print('_____Tamanho do Time_____', len(lista_original))
    for linha in lista_original:
        if re.match(_pattern, linha):
            res = re.split(_pattern, linha)
            res_clear = [item.strip() for item in res if item.strip()]

            if len(res_clear) == 2:
                filtered.append({res_clear[0] : res_clear[1]})

    # TODO - Tirar time por cor
    # MAX_TIME=(int(number) - 1)
    # def times(lista, n):
    #     for i in range(0, len(lista), n):
    #         yield lista[i:i + n]

    # lista = list(times(lista=filtered, n=MAX_TIME))
    # print('LISTA COM SEPARACAO ', len(lista), lista)

    time1 = []
    time2 = []
    time3 = []
    time4 = []
    for jogador in filtered:
        time = random.randint(0, (int(number) - 1))

        if time == 0:
            jogador['time'] = 'Time: 1'
            time1.append(jogador)
        elif time == 1:
            jogador['time'] = 'Time: 2'
            time2.append(jogador)
        elif time == 2:
            jogador['time'] = 'Time: 3'
            time3.append(jogador)
        elif time == 3:
            jogador['time'] = 'Time: 4'
            time4.append(jogador)

    print('JOGADORES DEPOIS', filtered)
    return filtered

@app.route('/api/escolha', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_escolhidos():
    if request.method == 'POST':
        data = request.json
        print('| ---------- ESCOLHA POST ', data)

        jogadores = []
        for d in data['names'].splitlines():
            jogadores.append(d)

        filtrado = filter_escolha(jogadores, data['number'])
        # print('| == filtrado ==> ', filtrado)

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
