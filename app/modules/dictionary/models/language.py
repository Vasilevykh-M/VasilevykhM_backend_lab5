from sqlalchemy import Column, Integer, Text, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.common.db import Base

article_tag = Table('languages', Base.metadata,
                       Column('id_language', Integer, ForeignKey('language.id'),primary_key=True),
                       Column('id_author', Integer, ForeignKey('author.id'),primary_key=True))

class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key = True)
    language = Column(Text, nullable = True)
    books = relationship("Book")
    lg = relationship("Author", secondary = article_tag)

    def __init__(self, *args, **kwargs):
        super(Language, self).__init__(*args, **kwargs)