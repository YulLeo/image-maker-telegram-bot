from sqlalchemy import (BLOB, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)

from core.db import Base


class Images(Base):
    __tablename__ = "images"
    id = Column(String, primary_key=True, unique=True)
    date = Column(DateTime)
    picture = Column(BLOB)
    user_id = Column(Integer)


class GIFs(Base):
    __tablename__ = "gifs"
    id = Column(String, primary_key=True, unique=True)
    date = Column(DateTime)
    picture = Column(BLOB)
    user_id = Column(Integer, ForeignKey("images.user_id"))
    private = Column(Boolean)
