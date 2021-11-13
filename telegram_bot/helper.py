import sqlite3
from enum import Enum
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


class ArgsGetGifsEnum(Enum):
    my_gifs = '/download_my_gifs'
    all_gifs = '/download_all_gifs'


def add_to_archive(gifs: set) -> BytesIO:
    """
    Extracts gifs from sqllite rows, converts each image to bytes.
    Returns BytesIO zip file with gifs.
    :param gifs: set of BytesIO objects
    :return: BytesIO
    """
    zip = BytesIO()
    zip.name = ZIP_FILE_NAME
    with ZipFile(zip, "w") as zip_obj:
        for gif in gifs:
            zip_obj.writestr(gif.name, gif.read())
    zip.seek(0)
    return zip
