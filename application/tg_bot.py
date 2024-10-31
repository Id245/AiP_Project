import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router


load_dotenv()
token = os.getenv('API_TOKEN')
if token is None:
    raise ValueError("Нет токена бота")


bot = Bot(token=token)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
