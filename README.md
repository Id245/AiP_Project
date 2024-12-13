# AiP_Project

## Описание
Кей-логгер, стиллер т-даты, плейбой, филантроп

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/yourusername/AiP_Project.git
    ```

2. Перейдите в директорию проекта:
    ```sh
    cd AiP_Project
    ```

3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

## Настройка

1. Создайте файл [.env](http://_vscodecontentref_/1) в корне проекта и добавьте следующие переменные окружения:
    ```
    API_TOKEN=your_telegram_bot_api_token
    CHAT_ID=your_telegram_chat_id
    host=your_database_host
    user=your_database_user
    password=your_database_password
    db_name=your_database_name
    port=your_database_port
    ```

2. Убедитесь, что у вас установлен и настроен MySQL сервер.

## Использование

### Запуск Telegram бота

1. Перейдите в директорию [application](http://_vscodecontentref_/2):
    ```sh
    cd application
    ```

2. Запустите скрипт `tg_bot.py`:
    ```sh
    python tg_bot.py
    ```

### Запуск Malware

1. Перейдите в директорию [hacktool](http://_vscodecontentref_/3):
    ```sh
    cd hacktool
    ```

2. Запустите скрипт `malware.py`:
    ```sh
    python malware.py
    ```

## Структура проекта

- [application](http://_vscodecontentref_/4)
  - `tg_bot.py`: Основной скрипт для запуска Telegram бота.
  - `handlers.py`: Обработчики команд и сообщений для бота.
  - `keyboards.py`: Определение клавиатур для бота.
  - `sql_connect.py`: Подключение к базе данных.

- [hacktool](http://_vscodecontentref_/5)
  - `malware.py`: Скрипт для отслеживания нажатий клавиш и отправки данных.
  - `stiller.py`: Скрипт для архивирования данных и отправки их через Telegram.
  - `layout_mapping.py`: Словари для преобразования раскладок клавиатуры.
  - `sql_connect.py`: Подключение к базе данных.

## Зависимости

Проект использует следующие библиотеки:
- `aiogram`
- `python-dotenv`
- `pymysql`
- `pynput`

## Лицензия

Всё лицензированно, я проверил (погодите, это реально?...)
