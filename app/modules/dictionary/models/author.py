from sqlalchemy import Column, Integer, Text, Date
from sqlalchemy.orm import relationship

from app.common.db import Base


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key = True)
    fio = Column(Text, nullable = True)
    birthday = Column(Date, nullable = False)
    biography = Column(Text, nullable= False)
    books = relationship("Book")

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)