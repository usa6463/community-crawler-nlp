import os
from datetime import date, datetime, timedelta

from elasticsearch import Elasticsearch
from elasticsearch_dsl7 import Q
from elasticsearch_dsl7 import Search
from elasticsearch_dsl7 import connections
from konlpy.tag import Okt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_migration.models.morpheme_info import MorphemeInfo

PGSQL_URL = os.getenv("PGSQL_URL")
ES_URL = os.getenv("ES_URL")

# ES connection
connections.create_connection(hosts=[ES_URL], timeout=60)
client = Elasticsearch()

# Postgresql connection
pgsql_engine = create_engine(PGSQL_URL)
pgsql_session = sessionmaker(pgsql_engine)

target_dt = os.getenv("TARGET_DT")
q = Q('match', dt=target_dt)
s = Search().extra(track_total_hits=True).sort('dt').using(client).query(q)
response = s.execute()
hit_count = s.count()

for h in s[0:hit_count]:
    print(h.title, h.dt, h.url, h.content, h.replyList)

print(f"num: {s.count()}")

# we can now construct a Session() and include begin()/commit()/rollback()
# at once
with pgsql_session.begin() as session:
    target_dt_obj = datetime.strptime(target_dt, "%Y-%m-%d")
    target_dt_str = target_dt_obj.strftime("%Y%m%d")
    target_dt_hyphen = target_dt_obj.strftime("%Y-%m-%d")
    next_dt_hyphen = (target_dt_obj + timedelta(days=1)).strftime("%Y-%m-%d")

    query = f"CREATE TABLE IF NOT EXISTS morpheme_info_{target_dt_str} PARTITION OF morpheme_info FOR VALUES FROM ('{target_dt_hyphen}') TO ('{next_dt_hyphen}');"
    print(query)

    session.execute(query)
    row = MorphemeInfo(
        log_date=target_dt_obj,
        word="test",
        morpheme="Noun",
        url="localhost",
        community_type="DC",
        content_type="Hello"
    )
    session.add_all([row])
    # 어떤 포맷을 write 해야할 것인가
    print("test")
# commits the transaction, closes the session

okt = Okt()
print(okt.morphs('단독입찰보다 복수입찰의 경우'))
print(okt.pos(u'고맙다 !! 덕분에 안사기로 결정했다 !!', norm=True))
