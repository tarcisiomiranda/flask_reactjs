from mysql.connector import errorcode
from colorama import init, Fore
import mysql.connector
import os
import sys
import time
import json
import re


# Inicializar a biblioteca colorama
init()

class MySQLAddOn:

    def __init__(self):
        """
            General configurations
        """
        if len(sys.argv) > 1:
            self.syndic = sys.argv[1]
        else:
            self.syndic = None
        self.url_git = False
        self.set_grains_hip = False
        self.fullpath = os.path.abspath(os.path.dirname(__file__))
        multi_env = os.getenv('DATABASE_SI', False)

        # Multi-line params
        self.conn_dict = {}
        if bool(multi_env) == True:
            print('|---> Usando o Kwarg com Multiline-Parameters! <---|')
            TRANSLATE_MAP = {
                'user': 'si_MYSQL_USER',
                'password': 'si_MYSQL_PASSWORD',
                'host': 'si_MYSQL_HOST',
                'port': 'si_MYSQL_PORT',
                'database': 'si_MYSQL_DATABASE',
            }

            for f_data in multi_env.splitlines():
                f_data = f_data.split('=')
                # pegando a instrucao para setar os grains
                if f_data[0] == 'si_SET_GRAINS_HIP':
                    if f_data[1].lower() == 'true':
                        self.set_grains_hip = True
                # dados para conexao do banco
                for map_data in TRANSLATE_MAP.items():
                    if len(f_data) == 2 and f_data[0] in map_data[1]:
                        self.conn_dict.update({map_data[0]: f_data[1]})

            try:
                self.conn = mysql.connector.connect(**self.conn_dict)
                self.conn.autocommit = True
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)

        elif os.path.exists('{}/secret_data.txt'.format(self.fullpath)):
            print('|---> Usando o Kwarg do Arquivo! <---|')
            conn_dict = {}
            TRANSLATE_MAP = {
                'user': 'si_MYSQL_USER',
                'password': 'si_MYSQL_PASSWORD',
                'host': 'si_MYSQL_HOST',
                'port': 'si_MYSQL_PORT',
                'database': 'si_MYSQL_DATABASE',
            }
            try:
                with open('{}/secret_data.txt'.format(self.fullpath), 'r') as file:
                    file_db = file.read()
                    file.close()

                for f_data in file_db.splitlines():
                    f_data = f_data.split('=')

                    for map_data in TRANSLATE_MAP.items():
                        if len(f_data) == 2 and f_data[0] in map_data[1]:
                            conn_dict.update({map_data[0]: f_data[1]})
                        # pegando a instrucao para setar os grains
                        if len(f_data) == 2 and f_data[0] == 'si_SET_GRAINS_HIP':
                            if f_data[1].lower() == 'true':
                                self.set_grains_hip = True
                        if len(f_data) == 2 and f_data[0] == 'si_GIT_RAW_CSV':
                                self.url_git = f_data[1]

                self.conn = mysql.connector.connect(**conn_dict)
                self.conn.autocommit = True

            except mysql.connector.Error as err:
                print(f'{Fore.RED} Error DB: {err}')

        # One-line params
        else:
            print('|---> Usando o conexao direta! <---|')
            database_host = os.getenv('si_MYSQL_HOST', False)
            database_name = os.getenv('si_MYSQL_DATABASE', False)
            database_user = os.getenv('si_MYSQL_USER', False)
            database_pass = os.getenv('si_MYSQL_PASSWORD', False)
            self.conn = mysql.connector.connect(
                host=database_host,
                database=database_name,
                user=database_user,
                password=database_pass
            )
            self.conn.autocommit = True

            # pegando a instrucao para setar os grains
            if bool(os.getenv('si_SET_GRAINS_HIP')):
                if os.getenv('si_SET_GRAINS_HIP').lower() == 'true':
                    self.set_grains_hip = True

# call file
if __name__ == '__main__':
    MySQLAddOn().load_data()
    MySQLAddOn().conn.close()
