FROM registry.cn-hangzhou.aliyuncs.com/limingmax-test/ai-base-trend:v2

ENV LANG C.UTF-8

ADD hbase.keytab /etc
ADD krb5.conf /etc

COPY trend /service/trend
ADD start.sh /service/trend/src
RUN chmod -R 777 /service/trend/src/start.sh


WORKDIR /service/trend/src

CMD ["/service/trend/src/start.sh"]
#防docker容器自动退出
ENTRYPOINT tail -f /dev/null
