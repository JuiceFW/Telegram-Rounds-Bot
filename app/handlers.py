from pathlib import Path
import traceback
import datetime
import logging
import sys
import os

from aiogram.types import Message, FSInputFile, ReplyParameters
from aiogram.filters import CommandStart
from aiogram import Router, F, Bot


logger = logging.getLogger(__name__)
router = Router()


BASE_DIR = Path(sys.argv[0]).parent
DOWNLOADS_DIR = BASE_DIR.joinpath("Downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    text = """
<b>Привет{user_creds}!</b>

<i>Спасибо за использование {bot_name}!
Этот бот поможет тебе получить кружочек из своего видео или голосовое из своего аудио.
Чтобы бот начал рабоать - просто отправь мне видео формата кружочка или файл с аудио!

made by <a href="https://t.me/juiceworks">Juice</a>, @{bot_username}!</i>
"""

    user_creds = ""
    if message.from_user.username:
        user_creds = f", @{message.from_user.username}"
    elif message.from_user.first_name:
        user_creds = f", {message.from_user.first_name}"

    me = await bot.get_me()
    await message.answer(
            text.format(
                user_creds=user_creds,
                bot_name=me.full_name,
                bot_username=me.username
            ),
            parse_mode='html',
            disable_web_page_preview=True
        )


@router.message(lambda message: message.audio)
async def handle_audio(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, "upload_audio")

    audio = message.audio
    file_id = audio.file_id
    msg = await bot.send_message(
        message.chat.id,
        "<b>Аудио найдено! Начинаю обработку...</b>",
        reply_parameters=ReplyParameters(message_id=message.message_id),
        parse_mode='html'
    )

    file = await bot.get_file(file_id)

    # date = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
    uniq_name = f"{message.chat.id}_{file_id}.mp3"

    try:
        file_path = str(DOWNLOADS_DIR.joinpath(uniq_name))
        await bot.download_file(file.file_path, file_path)

        audio_file = FSInputFile(file_path)
        await message.reply_voice(voice=audio_file)
    except Exception as ex:
        if "VOICE_MESSAGES_FORBIDDEN" in str(ex):
            logger.error(str(ex) + f". Chat_id: {message.chat.id}")

            text = """
<b>❌ Ошибка отправки аудио!</b>

<i>Кажется, в Ваших настройках стоит запрет на отправку голосовых сообщений!</i>

<b>Пожалуйста, добавьте бота в список исключений, или уберите запрет.</b>"""
            await bot.send_message(
                message.chat.id,
                text,
                reply_parameters=ReplyParameters(message_id=message.message_id),
                parse_mode='html'
            )
        else:
            logger.error(traceback.format_exc())
    finally:
        os.remove(file_path)

    try:
        await bot.delete_message(message.chat.id, msg.message_id)
    except:
        logger.error(traceback.format_exc())

    
@router.message(lambda message: message.video)
async def handle_video_note(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, "upload_video_note")

    video = message.video
    file_id = video.file_id
    msg = await bot.send_message(
        message.chat.id,
        "<b>Видео найдено! Начинаю обработку...</b>",
        reply_parameters=ReplyParameters(message_id=message.message_id),
        parse_mode='html'
    )

    file = await bot.get_file(file_id)

    # date = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
    uniq_name = f"{message.chat.id}_{file_id}.mp4"

    try:
        file_path = str(DOWNLOADS_DIR.joinpath(uniq_name))
        await bot.download_file(file.file_path, file_path)

        video_note = FSInputFile(file_path)
        await message.reply_video_note(video_note=video_note)
    except Exception as ex:
        if "VOICE_MESSAGES_FORBIDDEN" in str(ex):
            logger.error(str(ex) + f". Chat_id: {message.chat.id}")

            text = """
<b>❌ Ошибка отправки видео!</b>

<i>Кажется, в Ваших настройках стоит запрет на отправку голосовых сообщений!</i>

<b>Пожалуйста, добавьте бота в список исключений, или уберите запрет.</b>"""
            await bot.send_message(
                message.chat.id,
                text,
                reply_parameters=ReplyParameters(message_id=message.message_id),
                parse_mode='html'
            )
        else:
            logger.error(traceback.format_exc())
    finally:
        os.remove(file_path)

    try:
        await bot.delete_message(message.chat.id, msg.message_id)
    except:
        logger.error(traceback.format_exc())


@router.message()
async def msg_filter(message: Message, bot: Bot):
    if message.chat.type != "private": return

    text = """
<b>❌ Кажется, это не видео!

Пожалуйста, попробуйте повторить попытку, отправив видео без сжатия!</b>"""
    await bot.send_message(
        message.chat.id,
        text,
        reply_parameters=ReplyParameters(message_id=message.message_id),
        parse_mode='html'
    )
