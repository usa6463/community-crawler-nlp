from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class MorphemeInfo(Base):
    __tablename__ = "morpheme_info"
    __table_args__ = {
        'postgresql_partition_by': 'RANGE (log_date)'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    log_date = Column(Date, primary_key=True)
    word = Column(String, nullable=False)
    morpheme = Column(String, nullable=False)
    url = Column(String, nullable=False)
    community_type = Column(String, nullable=False) # 커뮤니티 사이트 종류
    content_type = Column(String, nullable=False) # 게시글인지 댓글인지, 대댓글인지