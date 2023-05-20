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

class ConfigScheduler:
    SCHEDULER_API_ENABLED = True

''' Start Flask and Scheduler '''
app = Flask(__name__)
CORS(app)
scheduler = APScheduler()

# def db():
#     my_sql = MySQLAddOn()
#     my_sql.conn.autocommit = True
#     cursor = my_sql.conn.cursor(dictionary=True)

#     return cursor

# API Rest
@app.route('/api/users', methods=['GET', 'POST', 'PUT'])
def get_users():
    # my_sql = MySQLAddOn()
    # # print('-----------> ', my_sql.__dict__)
    # my_sql.conn.autocommit = True
    # cursor = my_sql.conn.cursor(dictionary=True)
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

            # Executar a consulta
            cursor.execute(query, values)

            # Commit das alterações
            # conn.commit()

            return jsonify({'message': 'Usuário criado com sucesso'}), 201

        if request.method == 'PUT':
            # TODO
            my_sql = MySQLAddOn()
            my_sql.conn.autocommit = True
            cursor = my_sql.conn.cursor(dictionary=True)

            print('PUT > ', data)

            # query = "UPDATE users SET name = %s, email = %s, mobile = %s, birth_date = %s WHERE id = %s"
            # values = (data['name'], data['email'], data['mobile'], data['birth_date'], user_id)

            # Execute a query de atualização
            # cursor.execute(query, values)

            # name = data.get('name')
            # email = data.get('email')
            # fone = data.get('fone')
            # data_nascimento = data.get('data_nascimento')

            return 'Solicitação PUT recebida'

        elif request.method == 'GET':
            # TODO
            my_sql = MySQLAddOn()
            my_sql.conn.autocommit = True
            cursor = my_sql.conn.cursor(dictionary=True)

            users = 'SELECT * FROM users'
            cursor.execute(users)
            res = cursor.fetchall()

            return jsonify(res)

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
