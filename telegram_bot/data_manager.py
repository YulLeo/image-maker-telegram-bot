from core.db import session
from telegram_bot.helper import ArgsGetGifsEnum
from telegram_bot.models import GIFs
from minio import Minio
from minio.commonconfig import Tags

client = Minio(
    "127.0.0.1:9000",
    access_key="yuliya",
    secret_key="9817930789h",
    secure=False)


def get_gifs(user_id, amount: ArgsGetGifsEnum):
    all_bucket_objects = client.list_objects('gifs', include_user_meta=True)
    gifs = set()
    if amount == ArgsGetGifsEnum.all_gifs:
        for num, object in enumerate(all_bucket_objects):
            if object.metadata['X-Amz-Meta-Private'] == 'False' or object.metadata['X-Amz-Meta-User_id'] == str(user_id):
                retrieved_object = client.get_object('gifs', object.object_name)
                retrieved_object.name = f'num.gif'
                gifs.add(retrieved_object)
    if amount == ArgsGetGifsEnum.my_gifs:
        for num, object in enumerate(all_bucket_objects):
            if object.metadata['X-Amz-Meta-User_id'] == str(user_id):
                retrieved_object = client.get_object('gifs', object.object_name)
                retrieved_object.name = f'num.gif'
                gifs.add(retrieved_object)

    return gifs


def get_user_gifs(user_id):
    user_gifs = session.query(
        GIFs.picture).filter(
        GIFs.user_id == user_id).all()
    return user_gifs
