from io import BytesIO
from zipfile import ZipFile

from PIL import Image

from telegram_bot.config import ZIP_FILE_NAME


def read_image(picture):
    return Image.open(picture)


def read_images(pictures):
    return [Image.open(picture) for picture in pictures]


def add_to_archive(gifs):
    with BytesIO() as zip:
        zip.name = ZIP_FILE_NAME
        with ZipFile(zip, "w") as zip_obj:
            for num, gif in enumerate(gifs):
                zip_obj.writestr(f"{num}.gif", gif.picture)
        zip.seek(0)
        return zip
