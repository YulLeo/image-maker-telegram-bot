import io
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import insert

from core.db import session
from telegram_bot.data_manager import add_table_row
from telegram_bot.models import GIFs


def read_images(pictures):
    if type(pictures) is not list:
        return Image.open(pictures)
    else:
        return [Image.open(picture) for picture in pictures]


def add_text_to_picture(img, text: str, user_id):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("AbyssinicaSIL-Regular.ttf", 20)
    w, h = draw.textsize(text)
    # width, height = (img.size[0] - w) * 0.5, (img.size[1] - h) * 0.5
    # width, height = (img.size[0] - w) * 0.5, (img.size[1] - h) * 0.1
    width, height = (img.size[0] - w) * 0.5, (img.size[1] - h) * 0.9
    draw.text((width, height), text, 0, font=font)
    new_image = io.BytesIO()
    new_image.name = "image_with_text.png"
    img.save(new_image, format="PNG")
    add_table_row("images", user_id, new_image)
    new_image.seek(0)
    return new_image
