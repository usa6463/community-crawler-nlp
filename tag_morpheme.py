import os

from elasticsearch_dsl7 import connections
from elasticsearch_dsl7 import Search
from elasticsearch import Elasticsearch
from konlpy.tag import Okt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from elasticsearch_dsl7 import Q

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

target_dt = os.getenv("TARGET_DT")
q = Q('match', dt=target_dt)
s = Search().extra(track_total_hits=True).sort('dt').using(client).query(q)
response = s.execute()
hit_count = s.count()

for h in s[0:hit_count]:
    print(h.title, h.dt, h.url)

print(f"num: {s.count()}")

# we can now construct a Session() and include begin()/commit()/rollback()
# at once
with pgsql_session.begin() as session:
    print("test")
# commits the transaction, closes the session

okt = Okt()
print(okt.morphs('단독입찰보다 복수입찰의 경우'))
print(okt.pos(u'고맙다 !! 덕분에 안사기로 결정했다 !!', norm=True))
