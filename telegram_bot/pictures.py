import io

from PIL import ImageDraw, ImageFont

from telegram_bot.config import REGULAR_TTF, SIZE, PNG_IMAGE, PNG
from telegram_bot.data_manager import add_table_row


def add_text_to_picture(img, text: str, user_id):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(REGULAR_TTF, SIZE)
    width_txt, height_txt = draw.textsize(text)
    width, height = (img.size[0] - width_txt) * 0.5, \
                    (img.size[1] - height_txt) * 0.9
    draw.text((width, height), text, 0, font=font)
    new_image = io.BytesIO()
    new_image.name = PNG_IMAGE
    img.save(new_image, format=PNG)
    add_table_row("images", user_id, new_image)
    new_image.seek(0)
    return new_image
