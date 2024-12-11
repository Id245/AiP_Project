from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import CommandStart
import keyboards as kb
# from db_utils import download_file_from_db

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    chat_id = message.chat.id
    with open('.env', 'a') as env_file:
        env_file.write(f'\nCHAT_ID={chat_id}')
    print(f'Сохранен CHAT_ID: {chat_id}')  # Отладочный принт
    await message.reply(f'Ваш chat_id: {chat_id}\nОн также сохранен для дальнейшего использования.', reply_markup=kb.main)

@router.message(F.text == '123')
async def send_file(message: Message):
    # Удалите или измените этот обработчик, так как он больше не нужен
    await message.reply('Функция отправки файла больше не используется.')