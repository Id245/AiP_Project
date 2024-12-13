from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import CommandStart
import keyboards as kb
from sql_connect import db_connector
from keyboards import get_users_from_bd  
router = Router()

selected_user = None  

@router.message(CommandStart())
async def start(message: Message):
    await message.reply('Список команд', reply_markup=kb.main)

@router.message(F.text == 'Выбрать пользователя')
async def choose_user(message: Message):
    keyboard = await kb.reply_db_users()
    await message.reply('Список пользователей', reply_markup=keyboard)

@router.message(lambda message: message.text in get_users_from_bd())
async def user_selected(message: Message):
    global selected_user
    selected_user = message.text
    await message.reply(f'Вы выбрали пользователя: {selected_user}', reply_markup=kb.user_actions)

@router.message(F.text == 'Получить логи')
async def get_logs(message: Message):
    global selected_user
    print('selected_user')
    if selected_user:
        connection = db_connector()
        cursor = connection.cursor()
        cursor.execute('SELECT content FROM users_data WHERE username = %s', (selected_user,))
        result = cursor.fetchone()
        print(result)
        if result:
            await message.reply(f'Логи пользователя {selected_user}:\n{result[0]}')
        else:
            await message.reply(f'Логи для пользователя {selected_user} не найдены.')
    else:
        await message.reply('Сначала выберите пользователя.')
