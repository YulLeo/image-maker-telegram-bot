import os
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
# PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")
# PROXY_AUTH = aiohttp.BasicAuth(
#     login=os.getenv("TELEGRAM_PROXY_LOGIN"),
#     password=os.getenv("TELEGRAM_PROXY_PASSWORD")
# )
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
REPOSITORY_ROOT = Path(__file__).parent.parent
DATABASE_URL = (
    f"sqlite:///{REPOSITORY_ROOT}/{os.getenv('SQLALCHEMY_DATABASE_URL')}"
)
