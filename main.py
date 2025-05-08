from pathlib import Path
import traceback
import datetime
import logging
import asyncio
import sys
import os

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from app.handlers import router
from config import *


### SCRIPT TelegramRoundsBot ###
BASE_DIR = Path(sys.argv[0]).parent
LOGS_DIR = BASE_DIR.joinpath('Logs')


os.makedirs(LOGS_DIR, exist_ok=True)
logs_file = LOGS_DIR.joinpath(datetime.datetime.now().strftime("%d_%m_%Y") + ".log")

logs = os.listdir(LOGS_DIR)
logs = sorted(logs, key=lambda a: datetime.datetime.strptime(a.replace(".log", ""), "%d_%m_%Y"))

if len(logs) > 15:
    for item in logs:
        try:
            os.remove(LOGS_DIR.joinpath(item))
        except:
            print(traceback.format_exc())
            continue
logs = []

logger = logging.getLogger()
logging_format = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=logging_format
)
try:
    fh = logging.FileHandler(
        logs_file,
        encoding='utf-8'
    )
except:
    try:
        fh = logging.FileHandler(
            logs_file
        )
    except:
        print(traceback.format_exc())
        os._exit(0)
fh.setFormatter(logging.Formatter(logging_format))
logger.addHandler(fh)


dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN)


async def main():
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Exiting...")
