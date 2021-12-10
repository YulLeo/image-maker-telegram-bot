from telegram_bot.config import OBJECT_STORAGE_IP, OBJECT_STORAGE_PORT, ACCESS_KEY, SECRET_KEY
from telegram_bot.data_manager import MinioStore

minio_storage_manager = MinioStore(
    api=OBJECT_STORAGE_IP,
    port=OBJECT_STORAGE_PORT,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
)