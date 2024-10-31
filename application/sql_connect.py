import pymysql
from pymysql import Error
import os
from dotenv import load_dotenv

load_dotenv()


def db_connector():

    try:
        connection = pymysql.connect(
            host = os.getenv('host'),
            port = int(os.getenv('port')),
            user = os.getenv('user'),
            password = os.getenv('password'),
            database = os.getenv('db_name')
            )
        
        print('Успешое подключение к базе MySQL')
        return connection
    except Error as e:
        print(f"Ошибка подключения к базе MySQL: {e}")
        return
