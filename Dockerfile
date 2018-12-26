FROM registry.cn-hangzhou.aliyuncs.com/limingmax-test/ai-base:v1

ENV REDIS_IP REDIS_IP
ENV REDIS_PORT REDIS_PORT

ENV HBASE_IP HBASE_IP
ENV HBASE_PORT HBASE_PORT

COPY trend /service/trend
ADD start.sh /service/trend/src
RUN chmod -R 777 /service/trend/src/start.sh

WORKDIR /service/trend/src

CMD ["/service/trend/src/start.sh"]

ENTRYPOINT tail -f /dev/null
