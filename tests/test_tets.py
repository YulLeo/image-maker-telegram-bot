from io import BytesIO

import pytest
from PIL import Image, ImageChops, ImageSequence

from telegram_bot.config import PNG_IMAGE, PNG, GIF_FILE_NAME
from telegram_bot.helper import read_images
from telegram_bot.image_maker import resize_picture, add_text, save_file, save_gif, add_watermark


@pytest.fixture()
def picture_to_pil_provider():
    pictures = ['pictures_tests/_117310488_16.jpg',
                'pictures_tests/france-in-pictures.jpg']
    return read_images(pictures)


def test_add_watermark_equal():
    gif_1 = 'pictures_tests/test_gif_without_watermark.gif'
    gif_2 = Image.open('pictures_tests/test_gif_with_watermark.gif')
    with_water = add_watermark(gif_1, '@Yulia_Penkovskaya')
    l_1 = next(ImageSequence.Iterator(with_water))
    l_2 = next(ImageSequence.Iterator(gif_2))
    opened_frame1 = Image.open(l_1)
    assert ImageChops.difference(opened_frame1, l_2).getbbox() is None
    l_1 = next(ImageSequence.Iterator(with_water))
    l_2 = next(ImageSequence.Iterator(gif_2))
    opened_frame1 = Image.open(l_1)
    assert ImageChops.difference(opened_frame1, l_2).getbbox() is None


def test_save_gif(picture_to_pil_provider):
    gif = save_gif(picture_to_pil_provider)
    assert isinstance(gif, BytesIO)
    assert gif.name == GIF_FILE_NAME


def test_save_file():
    i_1 = Image.open('pictures_tests/france-in-pictures.jpg')
    new_image = save_file(i_1, PNG_IMAGE, PNG)
    assert isinstance(new_image, BytesIO)
    assert new_image.name == PNG_IMAGE


def test_add_text_true():
    i_1 = Image.open('pictures_tests/france-in-pictures.jpg')
    add_text(i_1, 'test test')
    new_image = save_file(i_1, PNG_IMAGE, PNG)
    i_2 = Image.open(new_image)
    assert ImageChops.difference(i_1, i_2).getbbox() is None


def test_add_text_false():
    i_1 = Image.open('pictures_tests/france-in-pictures.jpg')
    add_text(i_1, 'test test')
    save_file(i_1, PNG_IMAGE, PNG)
    i_3 = Image.open('pictures_tests/text_small.jpg')
    with pytest.raises(ValueError, match='images do not match'):
        ImageChops.difference(i_1, i_3).getbbox()


def test_resize_picture_different_size_images(picture_to_pil_provider):
    assert picture_to_pil_provider[0].size[0] > picture_to_pil_provider[1].size[0]
    assert picture_to_pil_provider[0].size[1] > picture_to_pil_provider[1].size[1]
    resized_pictures = resize_picture(picture_to_pil_provider)
    assert resized_pictures[0].size[0] == resized_pictures[1].size[0]
    assert resized_pictures[0].size[1] == resized_pictures[1].size[1]
