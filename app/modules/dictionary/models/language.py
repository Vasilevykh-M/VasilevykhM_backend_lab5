from sqlalchemy import Column, Integer, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.common.db import Base

class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key = True)
    language = Column(Text, nullable = True)
    books = relationship("Book")

    def __init__(self, *args, **kwargs):
        super(Language, self).__init__(*args, **kwargs)