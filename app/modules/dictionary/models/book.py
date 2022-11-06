from sqlalchemy import Column, Integer, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.common.db import Base


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key = True)
    name_book = Column(Text, nullable = True)
    year_book = Column(Date, nullable = False)
    id_language = Column(Integer, ForeignKey('language.id'), nullable = True)
    id_author = Column(Integer, ForeignKey('author.id'), nullable = True)
    state_read = Column(Boolean, nullable= False)

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)