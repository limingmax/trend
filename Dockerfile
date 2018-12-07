FROM bitnami/python:3.6.7
LABEL Author="wangrui<cfwr1991@126.com>"

ENV KAFKA_IP KAFKA_IP
ENV KAFKA_PORT KAFKA_PORT
ENV CONSUMER_TOPIC CONSUMER_TOPIC
ENV PRODUCER_TOPIC PRODUCER_TOPIC

ENV HBASE_IP HBASE_IP
ENV HBASE_PORT HBASE_PORT


ENV REDIS_IP REDIS_IP
ENV REDIS_PORT REDIS_PORT

COPY threshold /service/threshold
WORKDIR /service/threshold/src

ADD start.sh /service/threshold/src
RUN chmod -R 777 /service/threshold/src/start.sh

RUN pip install -r /service/threshold/src/requirements.txt

CMD ["/service/threshold/src/start.sh"]

ENTRYPOINT tail -f /dev/null