from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import CommandStart
import keyboards as kb

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.reply('123', reply_markup=kb.main)

@router.message(F.text == '123')
async def start(message: Message):
    keyboard = await kb.reply_db_users()
    await message.reply('It is not a cybercrime if you didnt get caught', reply_markup=keyboard)