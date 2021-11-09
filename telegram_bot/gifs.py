from io import BytesIO
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageSequence

from telegram_bot.config import REGULAR_TTF, RGBA, WIDTH_PROPORTION, \
    HEIGHT_PROPORTION, FILL_COLOR, STROKE_COLOR, GIF, DURATION, \
    STROKE_WIDTH, GIF_FILE_NAME

from telegram_bot.data_manager import add_table_row


def create_gif(pictures: list[Image], watermark: str, user_id: int, private=False) -> BytesIO:
    """
    Creates gif with watermark from list of PIL images
    :param pictures: list of PIL.Image objects
    :param watermark: watermark text, takes from user name
    :param user_id: user id
    :param private: defsult False, points out if the gif
    available for download by other users
    :return: BytesIO object
    """
    resized_pictures = resize_picture(pictures)
    gif = BytesIO()
    resized_pictures[0].save(
        gif,
        format=GIF,
        save_all=True,
        append_images=resized_pictures[1:],
        duration=DURATION,
        loop=0,
    )
    gif.seek(0)
    watermarked_gif = add_watermark(gif, watermark)
    add_table_row("gifs", user_id, watermarked_gif, private=private)
    watermarked_gif.seek(0)

    return watermarked_gif


def add_watermark(gif: BytesIO, watermark: str) -> BytesIO:
    """
    Add watermark to gif
    :param gif: gif as BytesIO object
    :param watermark: watermark text
    :return: BytesIO object
    """
    gif_opened = Image.open(gif)

    frames = []
    for frame in ImageSequence.Iterator(gif_opened):
        frame = frame.convert(RGBA)
        draw_frame = ImageDraw.Draw(frame)
        width_text, height_text = draw_frame.textsize(watermark)
        width, height = (gif_opened.size[0] - width_text) * WIDTH_PROPORTION, \
                        (gif_opened.size[1] - height_text) * HEIGHT_PROPORTION
        draw_frame.text(
            (width, height),
            watermark,
            fill=FILL_COLOR,
            stroke_width=STROKE_WIDTH,
            stroke_fill=STROKE_COLOR,
            font=make_dynamic_font(frame, watermark),
        )
        del draw_frame

        frames.append(frame)

    watermarked_gif = BytesIO()
    watermarked_gif.name = GIF_FILE_NAME
    frames[0].save(
        watermarked_gif, format=GIF, save_all=True, append_images=frames[1:]
    )
    watermarked_gif.seek(0)
    return watermarked_gif


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
    Adjusts all pictures in list to the smallest one
    :param pictures: list of PIL objects
    :return: list of PIL objects
    """
    base_width = min(picture.size[0] for picture in pictures)
    base_height = min(picture.size[1] for picture in pictures)

    return [
        picture.resize((base_width, base_height), Image.ANTIALIAS)
        for picture in pictures
    ]
