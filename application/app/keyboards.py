import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import pymysql
from config import host, user, password, db_name
from pymysql import Error

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='123')]
])

def get_users_from_bd():
    users_list = []
    try:
        with pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        ) as connection:
            print('Successfully connected to BD')
            cursor = connection.cursor()
            cursor.execute('SELECT USERNAME FROM users_data')
            users = cursor.fetchall()
            for user_data in users:
                users_list.append(''.join(list(user_data.values())))
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    
    return users_list

async def reply_db_users():
    keyboard1 = ReplyKeyboardBuilder()
    user_list = get_users_from_bd()
    for user in user_list:
        keyboard1.add(KeyboardButton(text=user))
    return keyboard1.adjust(1).as_markup()
