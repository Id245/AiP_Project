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
    """
    Обрабатывает команду /start.

    :param message: Сообщение с командой /start.
    :type message: aiogram.types.Message
    """
    await message.reply('Список команд', reply_markup=kb.main)

@router.message(F.text == 'Выбрать пользователя')
async def choose_user(message: Message):
    """
    Обрабатывает выбор пользователя.

    :param message: Сообщение с текстом "Выбрать пользователя".
    :type message: aiogram.types.Message
    """
    keyboard = await kb.reply_db_users()
    await message.reply('Список пользователей', reply_markup=keyboard)

@router.message(lambda message: message.text in get_users_from_bd())
async def user_selected(message: Message):
    """
    Обрабатывает выбор конкретного пользователя.

    :param message: Сообщение с именем пользователя.
    :type message: aiogram.types.Message
    """
    global selected_user
    selected_user = message.text
    await message.reply(f'Вы выбрали пользователя: {selected_user}', reply_markup=kb.user_actions)

@router.message(F.text == 'Получить логи')
async def get_logs(message: Message):
    """
    Обрабатывает запрос на получение логов.

    :param message: Сообщение с текстом "Получить логи".
    :type message: aiogram.types.Message
    """
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
        await message.reply('Сначала выберите пользователя.', reply_markup=await kb.reply_db_users())

@router.message(F.text == 'Список команд')
async def list_commands(message: Message):
    """
    Обрабатывает запрос на список команд.

    :param message: Сообщение с текстом "Список команд".
    :type message: aiogram.types.Message
    """
    await message.reply('Список команд', reply_markup=kb.all_commands)
