#!/bin/bash

set -x

sed -i "s/HBASE_IP/${HBASE_IP}/g" python.ini
sed -i "s/HBASE_PORT/${HBASE_PORT}/g" python.ini

sed -i "s/REDIS_IP:REDIS_PORT/${REDIS_IP}:${REDIS_PORT}/g" python.ini

sed -i "s/REALMS_KDC/${REALMS_KDC}/g" /etc/krb5.conf
sed -i "s/REALMS_ADMIN_SERVER/${REALMS_ADMIN_SERVER}/g" /etc/krb5.conf

python example_server.py
