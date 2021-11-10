import datetime

from sqlalchemy import (BLOB, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)

from core.db import Base, session


class Images(Base):
    __tablename__ = "images"
    id = Column(String, primary_key=True, unique=True)
    date = Column(DateTime)
    picture = Column(BLOB)
    user_id = Column(Integer)

    def __init__(self, picture, user_id):
        self.id = f"{self.user_id}{datetime.now()}"
        self.date = datetime.now()
        self.picture = picture
        self.user_id = user_id

    def add_table_row(self):
        session.add(self)
        session.commit()
        session.close()

    def delete_table_row(self):
        session.delete(self)
        session.commit()
        session.close()


class GIFs(Base):
    __tablename__ = "gifs"
    id = Column(String, primary_key=True, unique=True)
    date = Column(DateTime)
    picture = Column(BLOB)
    user_id = Column(Integer, ForeignKey("images.user_id"))
    private = Column(Boolean)

    def __init__(self, picture, user_id, private=False):
        self.id = f"{self.user_id}{datetime.now()}"
        self.date = datetime.now()
        self.picture = picture
        self.user_id = user_id
        self.private = private

    def add_table_row(self):
        session.add(self)
        session.commit()
        session.close()

    def delete_table_row(self):
        session.delete(self)
        session.commit()
        session.close()
