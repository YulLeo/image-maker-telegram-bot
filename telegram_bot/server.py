import logging
import os
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram.types import input_message_content
from aiogram_media_group import media_group_handler

from telegram_bot.config import API_TOKEN
from telegram_bot.data_manager import get_all_gifs, get_user_gifs
from telegram_bot.gifs import create_gif
from telegram_bot.pictures import add_text_to_picture, read_images

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "This bot assists you with pictures.\n"
        "Add text to your picture or make GIF from group of images\n\n"
        "Send picture with caption => Picture with text\n"
        "Send 2 to 10 pictures => GIF\n"
        "download_gifs: /download_gifs\n"
    )


@dp.message_handler(commands=["download_gifs"])
async def send_welcome(message: types.Message):
    await message.answer(
        "How many gifs?\n\n"
        "download all gifs: /download_all_gifs\n"
        "download my gifs: /download_my_gifs\n"
    )


@dp.message_handler(commands=["download_my_gifs"])
async def download_user_gifs(message: types.Message):
    user_id = message.from_user.id
    user_gifs = get_user_gifs(user_id)
    chat_id = message.chat.id
    if len(user_gifs) <= 10:
        await types.ChatActions.upload_photo()
        media = types.MediaGroup()
        for gif in user_gifs:
            b = BytesIO(gif.picture)
            media.attach_document(types.InputFile(b))
        await message.reply_media_group(media=media)
    else:
        zip_obj = ZipFile(f"{user_id}.zip", "w")
        for num, gif in enumerate(user_gifs):
            zip_obj.writestr(f"{num}.gif", gif.picture)

        await bot.send_document(chat_id, f"{user_id}.zip")
        os.remove(f"{user_id}.zip")


@dp.message_handler(commands=["download_all_gifs"])
async def download_all_gifs(message: types.Message):
    all_gifs = get_all_gifs()
    chat_id = message.chat.id
    user_id = message.from_user.id
    if len(all_gifs) <= 10:
        await types.ChatActions.upload_photo()
        media = types.MediaGroup()
        for num, gif in enumerate(all_gifs):
            b = BytesIO(gif.picture)
            b.name = f"{num}.gif"
            media.attach_document(types.InputFile(b))
        await message.reply_media_group(media=media)
    else:

        with BytesIO() as zip:
            zip.name = "gifs.zip"
            with ZipFile(zip, "w") as zip_obj:
                for num, gif in enumerate(all_gifs):
                    zip_obj.writestr(f"{num}.gif", gif.picture)
            zip.seek(0)
            await bot.send_document(chat_id, types.InputFile(zip))


@dp.message_handler(MediaGroupFilter(is_media_group=True), content_types=["photo"])
@media_group_handler
async def collect_media_group_photo(messages):
    downloaded_pictures = []

    for message in messages:
        b = BytesIO()
        downloaded_pictures.append(await message.photo[-1].download(destination_file=b))

    opened_pictures = read_images(downloaded_pictures)
    chat_id = messages[0].chat.id
    user_name = messages[0].from_user.mention
    user_id = messages[0].from_user.id
    await bot.send_animation(
        chat_id, animation=create_gif(opened_pictures, user_name, user_id)
    )


@dp.message_handler(content_types=["photo"])
async def handle_text_photo(message):
    user_id = message.from_user.id
    text = message.caption
    chat_id = message.chat.id
    b = BytesIO()
    downloaded_picture = await message.photo[-1].download(destination_file=b)
    opened_picture = read_images(downloaded_picture)
    await bot.send_photo(chat_id, photo=add_text_to_picture(opened_picture, text, user_id))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
