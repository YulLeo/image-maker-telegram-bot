from datetime import datetime

from core.db import session
from telegram_bot.models import GIFs, Images


def add_table_row(table_name, user_id, result, private: bool = False):
    models = {
        "gifs": GIFs(
            id=f'{user_id}{datetime.now()}',
            date=datetime.now(),
            user_id=user_id,
            picture=result.read(),
            private=private),
        "images": Images(
            id=f'{user_id}{datetime.now()}',
            date=datetime.now(),
            user_id=user_id,
            picture=result.read())
    }
    row = models[table_name]
    session.add(row)
    session.commit()


def get_all_gifs():
    all_gifs = session.query(
        GIFs.picture
    ).distinct(
        GIFs.picture
    ).filter(
        GIFs.private == False  # noqa: E712
    ).all()
    return all_gifs


def get_user_gifs(user_id):
    user_gifs = session.query(
        GIFs.picture
    ).filter(
        GIFs.user_id == user_id
    ).all()
    return user_gifs
