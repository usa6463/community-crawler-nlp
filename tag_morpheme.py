import logging
import os
from datetime import datetime, timedelta

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

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# log 출력
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.info(f"post count: {s.count()}")

okt = Okt()


def _extract_morpheme(content: str, community_type: str, content_type: str, target_dt: datetime, url: str) -> list:
    result = []
    for word in okt.pos(content, norm=True):
        row = MorphemeInfo(
            log_date=target_dt,
            word=word[0],
            morpheme=word[1],
            url=url,
            community_type=community_type,
            content_type=content_type
        )
        result.append(row)
    return result


with pgsql_session.begin() as session:
    target_dt_obj = datetime.strptime(target_dt, "%Y-%m-%d")
    target_dt_str = target_dt_obj.strftime("%Y%m%d")
    target_dt_hyphen = target_dt_obj.strftime("%Y-%m-%d")
    next_dt_hyphen = (target_dt_obj + timedelta(days=1)).strftime("%Y-%m-%d")

    drop_table_query = f"DROP TABLE IF EXISTS morpheme_info_{target_dt_str};"
    session.execute(drop_table_query)
    create_table_query = f"CREATE TABLE IF NOT EXISTS morpheme_info_{target_dt_str} PARTITION OF morpheme_info FOR VALUES FROM ('{target_dt_hyphen}') TO ('{next_dt_hyphen}');"
    session.execute(create_table_query)

    rows = []
    for h in s[0:hit_count]:

        rows.extend(
            _extract_morpheme(content=h.title, community_type='DC', content_type='title', target_dt=target_dt_obj,
                              url=h.url))
        rows.extend(_extract_morpheme(content=h.content, community_type='DC', content_type='content',
                                      target_dt=target_dt_obj, url=h.url))

        # reply 처리
        for reply in h.replyList:
            rows.extend(_extract_morpheme(content=reply['content'], community_type='DC', content_type='reply',
                                          target_dt=target_dt_obj, url=h.url))

            # inner reply 처리
            for inner in reply['innerReplyList']:
                rows.extend(_extract_morpheme(content=inner['content'], community_type='DC', content_type='inner_reply',
                                              target_dt=target_dt_obj, url=h.url))

    session.add_all(rows)
