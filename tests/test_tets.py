import os
from pathlib import Path

import pytest

from telegram_bot.pictures import add_text_to_picture, create_gif


@pytest.fixture()
def file_with_gif():
    output_file = Path(__file__).parent / "outer_gif.gif"
    yield output_file
    os.remove("outer_gif.gif")


def test_gif(file_with_gif):
    pictures = ["index.jpeg", "index.png"]
    create_gif(file_with_gif, pictures)
    assert file_with_gif.is_file()


def test_add_text_to_picture():
    output_file = Path(__file__).parent / "text_image.jpg"
    picture = "index.jpeg"
    add_text_to_picture(picture, "text_image.jpg")
    assert output_file.is_file()
