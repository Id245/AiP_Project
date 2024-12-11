import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from aiogram.types import Message
from aiogram.filters import CommandStart

load_dotenv()

# Проверьте, загружен ли файл .env
if not load_dotenv():
    print("Файл .env не найден или не может быть загружен")

token = os.getenv('BOT_TOKEN')

# Добавьте отладочный вывод для проверки загрузки переменных окружения
print(f'Загружен токен: {token}')

if token is None:
    raise ValueError("Нет токена бота")

bot = Bot(token=token)
dp = Dispatcher()

@router.message(CommandStart())
async def start(message: Message):
    chat_id = message.chat.id
    with open('.env', 'a') as env_file:
        env_file.write(f'\nCHAT_ID={chat_id}')
    print(f'Сохранен CHAT_ID: {chat_id}')  # Отладочный принт
    await message.reply('Ваш chat_id сохранен.')

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
