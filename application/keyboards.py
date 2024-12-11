from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sql_connect import db_connector

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='123')]
])

def get_users_from_bd():
    users_list = []
    connection = db_connector()
    cursor = connection.cursor()
    cursor.execute('SELECT USERNAME FROM users_data')
    users = cursor.fetchall()
    for user_name in users:
        users_list.append(user_name[0]) # fetchall возвращает список кортежей, берем первый элемент кортежа
    return users_list

async def reply_db_users():
    keyboard1 = ReplyKeyboardBuilder()
    user_list = get_users_from_bd()
    for user in user_list:
        keyboard1.add(KeyboardButton(text=user))
    return keyboard1.adjust(1).as_markup()