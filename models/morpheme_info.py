from sqlalchemy import Column, Integer, String, DateTime

from base import Base


class User(Base):
    __tablename__ = "morpheme_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String)
    morpheme = Column(String)
    datetime = Column(DateTime)
    url = Column(String)
    community_type = Column(String)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
