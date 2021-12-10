import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_KEY = os.getenv("ACCESS_KEY")

OBJECT_STORAGE_IP = os.getenv("IN_DOCKER", "127.0.0.1")
OBJECT_STORAGE_PORT = os.getenv("OBJECT_STORAGE_PORT", "9000")

REPOSITORY_ROOT = Path(__file__).parent.parent

PNG = "PNG"
GIF = "GIF"

GIF_FILE_NAME = "water_gif.gif"
PNG_IMAGE = "image_with_text.png"
ZIP_FILE_NAME = "gifs.zip"

RGBA = "RGBA"
FILL_COLOR = "white"
STROKE_COLOR = "black"

DURATION = 350
STROKE_WIDTH = 4
SIZE = 20
HEIGHT_PROPORTION = 0.9
WIDTH_PROPORTION = 0.7

REGULAR_TTF = REPOSITORY_ROOT / "telegram_bot" / "fonts" / "AbyssinicaSIL-Regular.ttf"  # noqa: E501

USER_ID = "X-Amz-Meta-User_id"
PRIVATE = "X-Amz-Meta-Private"
