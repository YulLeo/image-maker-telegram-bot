import io
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont, ImageSequence

from telegram_bot.data_manager import add_table_row


def create_gif(pictures, text, user_id, private=False):
    resized_pictures = resize_picture(pictures)
    my_gif = io.BytesIO()
    resized_pictures[0].save(
        my_gif,
        format="GIF",
        save_all=True,
        append_images=resized_pictures[1:],
        duration=350,
        loop=0,
    )
    my_gif.seek(0)
    result = add_watermark(my_gif, text)
    add_table_row("gifs", user_id, result, private=private)
    result.seek(0)

    return result


def add_watermark(file_path, text: str):
    im = Image.open(file_path)

    frames = []
    for frame in ImageSequence.Iterator(im):
        fontsize = 1  # starting font size
        # portion of image width you want text width to be
        img_fraction = 0.40
        font = ImageFont.truetype("AbyssinicaSIL-Regular.ttf", fontsize)
        while font.getsize(text)[0] < img_fraction * frame.size[0]:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype("AbyssinicaSIL-Regular.ttf", fontsize)

        frame = frame.convert("RGBA")
        fill_color = (255, 255, 255)
        stroke_color = (0, 0, 0)

        d = ImageDraw.Draw(frame)
        w, h = d.textsize(text)
        width, height = (im.size[0] - w) * 0.7, (im.size[1] - h) * 0.9
        d.text(
            (width, height),
            text,
            fill=fill_color,
            stroke_width=4,
            stroke_fill=stroke_color,
            font=font,
        )
        del d

        frames.append(frame)
    watermarked_gif = io.BytesIO()
    watermarked_gif.name = "water_gif.gif"
    frames[0].save(
        watermarked_gif, format="GIF", save_all=True, append_images=frames[1:]
    )
    watermarked_gif.seek(0)
    return watermarked_gif


def resize_picture(pictures: list):
    base_width = min(picture.size[0] for picture in pictures)
    base_height = min(picture.size[1] for picture in pictures)

    return [
        picture.resize((base_width, base_height), Image.ANTIALIAS)
        for picture in pictures
    ]
