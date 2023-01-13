from konlpy.tag import Okt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# an Engine, which the Session will use for connection
# resources
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(engine)

# we can now construct a Session() and include begin()/commit()/rollback()
# at once
with Session.begin() as session:
  print("test")
# commits the transaction, closes the session

okt = Okt()
print(okt.morphs('단독입찰보다 복수입찰의 경우'))
print(okt.pos(u'고맙다 !! 덕분에 안사기로 결정했다 !!', norm=True))