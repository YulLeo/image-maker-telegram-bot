import sqlite3
from io import BytesIO
from typing import Any
from zipfile import ZipFile

from PIL import Image

from telegram_bot.config import ZIP_FILE_NAME


def read_image(image: Any) -> Image:
    """
    Open file as PIL object
    :param image: image or gif
    :return: Image
    """
    return Image.open(image)


def read_images(images: list) -> list:
    """
    Open each file in list as PIL object
    :param images: list of images
    :return: Image
    """
    return [Image.open(picture) for picture in images]


def add_to_archive(rows_with_gifs: sqlite3.Row) -> BytesIO:
    """
    Extracts gifs from sqllite rows, converts each image to bytes.
    Returns BytesIO zip file with gifs.
    :param rows_with_gifs:
    :return: BytesIO
    """
    with BytesIO() as zip:
        zip.name = ZIP_FILE_NAME
        with ZipFile(zip, "w") as zip_obj:
            for num, gif in enumerate(rows_with_gifs):
                zip_obj.writestr(f"{num}.gif", gif.picture)
        zip.seek(0)
        return zip
