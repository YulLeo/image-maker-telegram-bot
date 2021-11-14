import logging
from io import BytesIO
from typing import Tuple

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_media_group import media_group_handler

from telegram_bot import exceptions
from telegram_bot.config import API_TOKEN, REPOSITORY_ROOT
from telegram_bot.data_manager import minio_storage_manager
from telegram_bot.helper import (ArgsGetGifsEnum, add_to_archive, read_image,
                                 read_images)
from telegram_bot.image_maker import create_gif, create_text_with_picture

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Pictures(StatesGroup):
    pictures = State()


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """Sends welcome message and help"""
    await message.answer(
        "This bot assists you with pictures.\n"
        "He can add text to your picture or make GIF from group of images\n\n"
        "Add text to picture: /add_text\n"
        "Create GIF: /create_gif\n"
        "Download_gifs: /download_gifs\n"
    )


@dp.message_handler(commands=["add_text"])
async def add_file_instructions(message: types.Message):
    """
    Explains how to add tex to image
    """
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=open(REPOSITORY_ROOT / "telegram_bot" / "add_text_example.png", "rb"),
        caption="Just attach picture and add your text in the same message",
    )


@dp.message_handler(commands=["create_gif"])
async def create_gif_instructions(message: types.Message):
    """
    Explains how to create GIF
    """
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=open(REPOSITORY_ROOT / "telegram_bot" / "private_gif_example.png", "rb"),
        caption="To make GIF you should attach group of images\nType 'private' to make GIF unavailable for "
        "downloading by other users",
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


@dp.message_handler(commands=["download_all_gifs", "download_my_gifs"])
async def download_gifs(message: types.Message):
    """
    Returns all gifs which weren't marked as private.
    If there are less or equal to ten gifs bot sends media group.
    If there are more than ten gifs, bot sends archive
    """
    try:
        gifs = minio_storage_manager.get_gifs(
            user_id=message.from_user.id, amount=ArgsGetGifsEnum(message.get_command())
        )

        await send_gifs(gifs, message)

    except exceptions.EmptyList as e:
        await message.answer(str(e))
        return


async def send_gifs(gifs: Tuple[int, list], message: types.Message):
    if gifs[0] == 0:
        raise exceptions.EmptyList(
            "There is no any GIFs to download. Let's create one /start"
        )
    elif gifs[0] == 1:
        await bot.send_animation(chat_id=message.chat.id, animation=gifs[1].pop())
    elif gifs[0] <= 10:
        media = await create_media_group(gifs[1])
        await message.reply_media_group(media=media)
    elif gifs[0] > 10:
        await bot.send_document(
            message.chat.id, types.InputFile(add_to_archive(gifs[1]))
        )


async def create_media_group(gifs: list[bytes]):
    media = types.MediaGroup()
    for gif in gifs:
        gif.name = "gif.gif"
        media.attach_document(types.InputFile(gif))
    return media


@dp.message_handler(MediaGroupFilter(is_media_group=True), content_types=["photo"])
@media_group_handler
async def collect_media_group_photo(messages, state: FSMContext):
    """
    Collects images from message with group of pictures and returns gif
    """
    async with state.proxy() as data:
        data["pictures"] = messages

    inline_mrkup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True).add(
        types.InlineKeyboardButton("yes", callback_data="btn_yes"),
        types.InlineKeyboardButton("no", callback_data="btn_no"),
    )

    await messages[-1].reply(
        "Should I make this GIF private?", reply_markup=inline_mrkup
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("btn"))
async def process_callback_kb1btn1(
    callback_query: types.CallbackQuery, state: FSMContext
):
    code = callback_query.data
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=types.InlineKeyboardMarkup([]),
    )
    downloaded_pictures = []
    async with state.proxy() as data:
        messages = data["pictures"]

    for message in messages:
        downloaded_pictures.append(
            await message.photo[-1].download(destination_file=BytesIO())
        )

    privacy = {"btn_yes": True, "btn_no": False}

    await bot.send_animation(
        chat_id=messages[0].chat.id,
        animation=create_gif(
            pictures=read_images(downloaded_pictures),
            watermark=messages[0].from_user.mention,
            user_id=messages[0].from_user.id,
            private=privacy[code],
        ),
    )


@dp.message_handler(content_types=["photo"])
async def handle_text_photo(message):
    """
    Takes picture and text and returns picture with text on it
    """
    downloaded_picture = await message.photo[-1].download(destination_file=BytesIO())
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=create_text_with_picture(
            img=read_image(downloaded_picture),
            text=message.caption,
            user_id=message.from_user.id,
        ),
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
