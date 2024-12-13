from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sql_connect import db_connector

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Выбрать пользователя')],
    [KeyboardButton(text='Список команд')]
])

user_actions = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить логи')],
    [KeyboardButton(text='Список команд')]
])

all_commands = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Выбрать пользователя')],
    [KeyboardButton(text='Получить логи')]
])

def get_users_from_bd():
    """
    Получает список пользователей из базы данных.

    :returns: Список пользователей из базы данных.
    :rtype: list
    :raises Error: Если не удается подключиться к базе данных.
    """
    users_list = []
    connection = db_connector()
    cursor = connection.cursor()
    cursor.execute('SELECT USERNAME FROM users_data')
    users = cursor.fetchall()
    for user_name in users:
        if user_name[0] is not None:
            users_list.append(user_name[0]) #fetchall возвращает список кортежкй, а поскольку у нас в столбце username одной строке соответствует одно имя, то создаётся идиотический кортеж из одного имени и запятой... Поэтому берем первый элемент кортежа
    return users_list

async def reply_db_users():
    """
    Создает клавиатуру с пользователями из базы данных.

    :returns: Клавиатура с пользователями.
    :rtype: ReplyKeyboardMarkup
    :raises Error: Если не удается подключиться к базе данных.
    """
    keyboard1 = ReplyKeyboardBuilder()
    user_list = get_users_from_bd()
    for user in user_list:
        keyboard1.add(KeyboardButton(text=user))
    keyboard1.add(KeyboardButton(text='Список команд'))
    return keyboard1.adjust(1).as_markup()
