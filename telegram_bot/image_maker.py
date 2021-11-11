from io import BytesIO
from typing import Any, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageSequence

from telegram_bot.config import (DURATION, FILL_COLOR, GIF, GIF_FILE_NAME,
                                 HEIGHT_PROPORTION, PNG, PNG_IMAGE,
                                 REGULAR_TTF, STROKE_COLOR, STROKE_WIDTH,
                                 WIDTH_PROPORTION)
from telegram_bot.helper import read_image
from telegram_bot.models import GIFs, Images


def create_gif(
        pictures: list, watermark: str,
        user_id: int, private=0) -> BytesIO:
    """
    Creates gif with watermark from list of PIL images and adds it to database.
    Returns BytesIO object
    :param pictures: list of PIL.Image objects
    :param watermark: watermark text, takes from user name
    :param user_id: user id
    :param private: defsult False, points out if the gif
    available for download by other users
    :return: BytesIO
    """
    resized_pictures = resize_picture(pictures)
    gif = save_gif(resized_pictures)
    watermarked_gif = add_watermark(gif, watermark)
    GIFs(watermarked_gif.read(), user_id, private).add_table_row()
    watermarked_gif.seek(0)
    return watermarked_gif


def add_watermark(gif: Any, watermark: str) -> BytesIO:
    """
    Add watermark to gif. Returns BytesIO object
    :param gif: gif file
    :param watermark: watermark text
    :return: BytesIO
    """
    gif_opened = read_image(gif)

    frames = []
    for frame in ImageSequence.Iterator(gif_opened):
        add_text(frame, watermark)
        frame = read_image(save_file(frame, GIF_FILE_NAME, GIF))
        frames.append(frame)

    return save_gif(frames)


def create_text_with_picture(img: Image, text: str, user_id: int) -> BytesIO:
    """
    Add text to PIL image, converts it to BytesIO object
    and add it to the database.
    :param img: opened PIL picture
    :param text: text to be added to the picture
    :param user_id: user id
    :return: BytesIO
    """
    add_text(img, text)
    new_image = save_file(img, PNG_IMAGE, PNG)
    Images(new_image.read(), user_id).add_table_row()

    new_image.seek(0)
    return new_image


def add_text(img: Image, text: str) -> ImageDraw:
    """
    Adds text to the image
    :param img: PiL image
    :param text: text to be added
    :return: ImageDraw
    """
    draw = ImageDraw.Draw(img)
    font = make_dynamic_font(img, text)
    draw.text(
        xy=(set_up_text_location(draw, img, text, font)),
        text=text,
        fill=FILL_COLOR,
        stroke_fill=STROKE_COLOR,
        stroke_width=STROKE_WIDTH,
        font=font,
    )
    return draw


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


def set_up_text_location(
    image: ImageDraw, img_opened: Image, text: str, font: ImageFont
) -> Tuple[Any, Any]:
    """
    Returns coordinates of text location on the image
    :param image: ImageDraw object
    :param img_opened: opened PIL image
    :param text: text
    :param font: ImageFont
    :return: Tuple[Any, Any]
    """
    width_text, height_text = image.textsize(text, font)
    width, height = (img_opened.size[0] - width_text) * WIDTH_PROPORTION, (
        img_opened.size[1] - height_text
    ) * HEIGHT_PROPORTION
    return width, height


def make_dynamic_font(image: Any, text: str) -> ImageFont:
    """
    Applies font size to image size
    :param image: image
    :param text: text
    :return: ImageFont
    """
    fontsize = 1
    img_fraction = 0.40
    font = ImageFont.truetype(REGULAR_TTF, fontsize)
    while font.getsize(text)[0] < img_fraction * image.size[0]:
        fontsize += 1
        font = ImageFont.truetype(REGULAR_TTF, fontsize)
    return font


def resize_picture(pictures: list) -> list:
    """
    Adjusts all pictures in list to the smallest one.
    Returns list of PIL objects.
    :param pictures: list of PIL objects
    :return: list
    """
    base_width = min(picture.size[0] for picture in pictures)
    base_height = min(picture.size[1] for picture in pictures)

    return [
        picture.resize((base_width, base_height), Image.ANTIALIAS)
        for picture in pictures
    ]
