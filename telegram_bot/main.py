import logging
from io import BytesIO

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram_media_group import media_group_handler

from telegram_bot.config import API_TOKEN
from telegram_bot.data_manager import get_all_gifs, get_user_gifs
from telegram_bot.gifs import create_gif
from telegram_bot.helper import read_image, add_to_archive, read_images
from telegram_bot.pictures import add_text_to_picture


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """Sends welcome message and help"""
    await message.answer(
        "This bot assists you with pictures.\n"
        "Add text to your picture or make GIF from group of images\n\n"
        "Send picture with caption => Picture with text\n"
        "Send 2 to 10 pictures => GIF\n"
        "download_gifs: /download_gifs\n"
    )


@dp.message_handler(commands=["download_gifs"])
async def download_gifs_options(message: types.Message):
    """
    Clarifies how many gifs must be downloaded
    """
    await message.answer(
        "How many gifs?\n\n"
        "download all gifs: /download_all_gifs\n"
        "download my gifs: /download_my_gifs\n"
    )


@dp.message_handler(commands=["download_my_gifs"])
async def download_user_gifs(message: types.Message):
    """
    Returns all gifs that were created by user, included private
    """

    user_gifs = get_user_gifs(user_id=message.from_user.id)
    if len(user_gifs) <= 10:
        media = types.MediaGroup()
        for gif in user_gifs:
            bytes_io_gif = BytesIO(gif.picture)
            media.attach_document(types.InputFile(bytes_io_gif))
        await message.reply_media_group(media=media)
    else:
        await bot.send_document(
            message.chat.id,
            types.InputFile(add_to_archive(user_gifs))
            )


@dp.message_handler(commands=["download_all_gifs"])
async def download_all_gifs(message: types.Message):
    """
    Returns all gifs which weren't marked as private.
    If there are less or equal to ten gifs bot sends media group.
    If there are more than ten gifs, bot sends archive
    """
    all_gifs = get_all_gifs()
    if len(all_gifs) <= 10:
        media = types.MediaGroup()
        for num, gif in enumerate(all_gifs):
            bytes_io_gif = BytesIO(gif.picture)
            bytes_io_gif.name = f"{num}.gif"
            media.attach_document(types.InputFile(bytes_io_gif))
        await message.reply_media_group(media=media)
    else:
        await bot.send_document(
            message.chat.id,
            types.InputFile(add_to_archive(all_gifs)))


@dp.message_handler(
    MediaGroupFilter(is_media_group=True), content_types=["photo"]
)
@media_group_handler
async def collect_media_group_photo(messages):
    """
    Collects images from message with group of pictures and returns gif
    """
    downloaded_pictures = []

    for message in messages:
        bytes_io_file = BytesIO()
        downloaded_pictures.append(
            await message.photo[-1].download(
                destination_file=bytes_io_file
            )
        )

    await bot.send_animation(
        chat_id=messages[0].chat.id,
        animation=create_gif(
            pictures=read_images(downloaded_pictures),
            text=messages[0].from_user.mention,
            user_id=messages[0].from_user.id
        )
    )


@dp.message_handler(content_types=["photo"])
async def handle_text_photo(message):
    """
    Takes picture and text and returns picture with text on it
    """
    bytes_io_file = BytesIO()
    downloaded_picture = await message.photo[-1].download(
        destination_file=bytes_io_file
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=add_text_to_picture(
            img=read_image(downloaded_picture),
            text=message.caption,
            user_id=message.from_user.id)
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
