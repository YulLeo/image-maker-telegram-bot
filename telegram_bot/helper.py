from enum import Enum
from io import BytesIO
from typing import Any
from zipfile import ZipFile

from PIL import Image

from telegram_bot.config import DURATION, GIF, GIF_FILE_NAME, ZIP_FILE_NAME


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
    """
    Enum class with arguments for get_gifs method
    """

    my_gifs = "/download_my_gifs"
    all_gifs = "/download_all_gifs"


def add_to_archive(gifs: list) -> BytesIO:
    """
    Extracts gifs from sqllite rows, converts each image to bytes.
    Returns BytesIO zip file with gifs.
    :param gifs: set of BytesIO objects
    :return: BytesIO
    """
    zip = BytesIO()
    zip.name = ZIP_FILE_NAME
    with ZipFile(zip, "w") as zip_obj:
        for num, gif in enumerate(gifs):
            gif.name = f"{num}.gif"
            zip_obj.writestr(gif.name, gif.read())
    zip.seek(0)
    return zip


def save_file(image: Image, name: str, file_format: str) -> BytesIO:
    """
    Takes PIL file and returns gif or image as BytesIO object
    :param file_format: file format
    :param name: file name
    :param image: PIL image
    :return: BytesIO
    """
    new_file = BytesIO()
    new_file.name = name
    image.save(new_file, format=file_format)
    return new_file


def save_gif(images: list) -> BytesIO:
    """
    Takes list of opened PIL images and returns gif as BytesIO object
    :param images: list of opened PIL images
    :return: BytesIO
    """
    gif = BytesIO()
    gif.name = GIF_FILE_NAME
    images[0].save(
        gif,
        format=GIF,
        save_all=True,
        append_images=images[1:],
        duration=DURATION,
        loop=0,
    )
    gif.seek(0)
    return gif
