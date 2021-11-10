from core.db import session
from telegram_bot.models import GIFs


def get_all_gifs():
    all_gifs = (
        session.query(GIFs.picture)
        .distinct(GIFs.picture)
        .filter(GIFs.private == False)  # noqa: E712
        .all()
    )
    return all_gifs


def get_user_gifs(user_id):
    user_gifs = session.query(
        GIFs.picture
    ).filter(
        GIFs.user_id == user_id
    ).all()
    return user_gifs
