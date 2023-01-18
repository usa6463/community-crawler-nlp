import os

from elasticsearch_dsl7 import connections
from elasticsearch_dsl7 import Search
from elasticsearch import Elasticsearch
from konlpy.tag import Okt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources
PGSQL_URL = os.getenv("PGSQL_URL")
ES_URL = os.getenv("ES_URL")
pgsql_engine = create_engine(PGSQL_URL)
# a sessionmaker(), also in the same scope as the engine
pgsql_session = sessionmaker(pgsql_engine)

# ES connection
connections.create_connection(hosts=[ES_URL], timeout=60)
client = Elasticsearch()
s = Search().using(client).query("match", title="목도리")
response = s.execute()
for hit in s:
    print(hit.title, hit.url)

# we can now construct a Session() and include begin()/commit()/rollback()
# at once
with pgsql_session.begin() as session:
    print("test")
# commits the transaction, closes the session

okt = Okt()
print(okt.morphs('단독입찰보다 복수입찰의 경우'))
print(okt.pos(u'고맙다 !! 덕분에 안사기로 결정했다 !!', norm=True))
