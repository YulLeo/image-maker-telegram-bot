import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
REPOSITORY_ROOT = Path(__file__).parent.parent
DATABASE_URL = (
    f"sqlite:///{REPOSITORY_ROOT}/{os.getenv('SQLALCHEMY_DATABASE_URL')}"  # noqa: E501
)

PNG = "PNG"

PNG_IMAGE = "image_with_text.png"

SIZE = 20

REGULAR_TTF = "AbyssinicaSIL-Regular.ttf"

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
