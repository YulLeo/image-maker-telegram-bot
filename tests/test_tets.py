from io import BytesIO

import pytest
from PIL import Image, ImageChops, ImageSequence

from telegram_bot.config import GIF_FILE_NAME, PNG, PNG_IMAGE
from telegram_bot.helper import read_images
from telegram_bot.image_maker import (add_text, add_watermark, resize_picture,
                                      save_file, save_gif)


@pytest.fixture()
def picture_to_pil_provider():
    pictures = [
        "pictures_tests/_117310488_16.jpg",
        "pictures_tests/france-in-pictures.jpg",
    ]
    return read_images(pictures)


def test_add_watermark_equal_gifs():
    gif_without_wat = "pictures_tests/test_gif_without_watermark.gif"
    sample_gif_with_wat = Image.open("pictures_tests/test_gif_with_watermark.gif")
    with_water = add_watermark(gif_without_wat, "@Yulia_Penkovskaya")
    gif_frame1 = next(ImageSequence.Iterator(with_water))
    gif_frame2 = next(ImageSequence.Iterator(sample_gif_with_wat))
    opened_frame1 = Image.open(gif_frame1)
    assert ImageChops.difference(opened_frame1, gif_frame2).getbbox() is None
    gif_without_wat = next(ImageSequence.Iterator(with_water))
    gif_with_wat = next(ImageSequence.Iterator(sample_gif_with_wat))
    opened_frame1 = Image.open(gif_without_wat)
    assert ImageChops.difference(opened_frame1, gif_with_wat).getbbox() is None


def test_save_gif(picture_to_pil_provider):
    gif = save_gif(picture_to_pil_provider)
    assert isinstance(gif, BytesIO)
    assert gif.name == GIF_FILE_NAME


def test_save_file():
    image_to_save = Image.open("pictures_tests/france-in-pictures.jpg")
    new_image = save_file(image_to_save, PNG_IMAGE, PNG)
    assert isinstance(new_image, BytesIO)
    assert new_image.name == PNG_IMAGE


def test_add_text_true():
    image_ver1 = Image.open("pictures_tests/france-in-pictures.jpg")
    add_text(image_ver1, "test test")
    new_image = save_file(image_ver1, PNG_IMAGE, PNG)
    image_ver2 = Image.open(new_image)
    assert ImageChops.difference(image_ver1, image_ver2).getbbox() is None


def test_add_text_false():
    image = Image.open("pictures_tests/france-in-pictures.jpg")
    add_text(image, "test test")
    save_file(image, PNG_IMAGE, PNG)
    different_image = Image.open("pictures_tests/text_small.jpg")
    with pytest.raises(ValueError, match="images do not match"):
        ImageChops.difference(image, different_image).getbbox()


def test_resize_picture_different_size_images(picture_to_pil_provider):
    image_big_width = picture_to_pil_provider[0].size[0]
    image_small_width = picture_to_pil_provider[1].size[0]
    assert image_big_width > image_small_width
    image_big_height = picture_to_pil_provider[0].size[1]
    image_small_height = picture_to_pil_provider[1].size[1]
    assert image_big_height > image_small_height
    resized_pictures = resize_picture(picture_to_pil_provider)
    resized_big_width = resized_pictures[0].size[0]
    resized_small_width = resized_pictures[1].size[0]
    assert resized_big_width == resized_small_width
    resized_big_height = resized_pictures[0].size[0]
    resized_small_height = resized_pictures[1].size[0]
    assert resized_big_height == resized_small_height
