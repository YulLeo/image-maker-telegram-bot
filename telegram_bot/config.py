import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

REPOSITORY_ROOT = Path(__file__).parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

ACCESS_KEY = os.getenv("ACCESS_KEY")

OBJECT_STORAGE_IP = os.getenv("IN_DOCKER", "127.0.0.1")

OBJECT_STORAGE_PORT = os.getenv("OBJECT_STORAGE_PORT", "9000")

PNG = "PNG"

PNG_IMAGE = "image_with_text.png"

SIZE = 20

REGULAR_TTF = REPOSITORY_ROOT / "telegram_bot" / "fonts" / "AbyssinicaSIL-Regular.ttf"  # noqa: E501

HEIGHT_PROPORTION = 0.9

WIDTH_PROPORTION = 0.7

RGBA = "RGBA"

FILL_COLOR = "white"

STROKE_COLOR = "black"

DURATION = 350

STROKE_WIDTH = 4

GIF = "GIF"

GIF_FILE_NAME = "water_gif.gif"

ZIP_FILE_NAME = "gifs.zip"
