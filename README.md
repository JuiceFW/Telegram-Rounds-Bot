
# Telegram Rounds Bot

Это Telegram-бот, написанный на Python с использованием библиотеки [aiogram](https://github.com/aiogram/aiogram).  
Проект реализует асинхронную обработку видео Telegram через Telegram Bot API, с последующей конвертацией в видео-кружочки.

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/JuiceFW/Telegram-Rounds-Bot.git
cd Telegram-Rounds-Bot
````

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте файл `config.py` в корневой директории проекта и добавьте в него ваш токен:

```python
# config.py
TOKEN = "your_bot_token"
```

> ⚠️ Не публикуйте свой токен в открытом доступе!

## Запуск

Для запуска бота выполните:

```bash
python main.py
```

## Зависимости

* Python 3.8+
* aiogram

Все зависимости указаны в `requirements.txt`.

## Лицензия

Этот проект распространяется под лицензией MIT.

```