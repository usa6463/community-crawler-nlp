FROM python:3.9.16

RUN pip install pipenv==2023.2.18
WORKDIR /tmp/community-crawler-nlp
COPY . /tmp/community-crawler-nlp
RUN pipenv install


ENV ES_URL="elasticsearch-master.default.svc.cluster.local"
ENV PG_SQL="postgresql://postgres:BuYEUUbplB@postgresql.postgresql.svc.cluster.local/community_info_provider"
ENV PYTHONUNBUFFERED="1"
ENV TARGET_DATE="2022-12-25"

#
#ENV LOGGING_LEVEL="info"
#ENV BOARD_BASE_URL="https://gall.dcinside.com/board/lists/?id=rlike"
#ENV ES_INDEX_NAME="dc-content-loglike"
#ENV WEB_DRIVER_PATH="/chromedriver"

ENTRYPOINT ["pipenv","run", "run_tag_morpheme"]
