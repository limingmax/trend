FROM registry.cn-hangzhou.aliyuncs.com/limingmax-test/ai-base:v3

ADD hbase.keytab /etc
ADD krb5.conf /etc

COPY trend /service/trend
ADD start.sh /service/trend/src
RUN chmod -R 777 /service/trend/src/start.sh

WORKDIR /service/trend/src

CMD ["/service/trend/src/start.sh"]

ENTRYPOINT tail -f /dev/null
