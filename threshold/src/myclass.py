# from zutils.zrpc.server.threadpool_server import ThreadpoolServer, AbstractServer
# from zutils.logger import Logger
import time
import datetime
import math
import happybase
import numpy as np
import json
from kafka import *
import configparser
import threading
data={}
class MyClass(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print("=====开始初始化=====")
        self.data =data
        cf = configparser.ConfigParser()
        cf.read("python.ini")
        self.kafka_host = cf.get("kafka", "host")
        self.kafka_port = cf.getint("kafka", "port")
        self.hbase_host = cf.get("hbase", "host")
        self.hbase_port = cf.getint("hbase", "port")
        self.consumer_topic=cf.get("kafka","consumer_topic")
        self.producer_topic=cf.get("kafka","producer_topic")
        # self.kafka_host = '192.168.212.71'  # kafka服务器地址
        # self.kafka_port = 9092  # kafka服务器端口
        # self.hbase_host='192.168.195.1'
        # self.hbase_port=9090
        print(self.kafka_host, self.kafka_port, self.hbase_host, self.hbase_port,self.consumer_topic,self.producer_topic)

        self.connection=happybase.Connection(self.hbase_host, self.hbase_port)
        self.producer=KafkaProducer(bootstrap_servers=['{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafka_host,
            kafka_port=self.kafka_port
        )],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.consumer=KafkaConsumer(
            # 'k8s_MonitorData',
            self.consumer_topic,
            # 'ai_threshold_alert',
            group_id='mygroup11',
            # auto_offset_reset='earliest',
            bootstrap_servers=['{kafka_host}:{kafka_port}'.format(kafka_host=self.kafka_host, kafka_port=self.kafka_port)],
            # 一定要设置下列两个参数。官网里有参数的解释https://kafka-python.readthed...
            # 主要是这句话：“ If no heartbeats are received by the broker before the expiration of this session timeout, then the broker will remove this consumer from the group and initiate a rebalance.”
            session_timeout_ms=6000,
            heartbeat_interval_ms=2000
        )
        print("====初始化完成====")
    def month_handle(self,year,month):
        year=int(year)
        month=int(month)
        if(month>1):
            month=month-1
            if(month>10):
                month=str(month)
            else:
                month='0'+str(month)
        else:
            year=year-1
            month='12'
        year=str(year)
        return year,month
    def run(self):
        self.consumer_metric()

    def select(self,metric, resource, namespace,year1,month1,day1, hour,pretime):
        # connection = self.connection
        connection = happybase.Connection(self.hbase_host, self.hbase_port)
        t = connection.table('Monitor_record')
        return_list = []
        result_list = []
        # TODO 这里pretime要处理一下大概
        pretime=int(pretime)
        if namespace:
            for i in range(pretime):
                year, month, day = self.time_handle(year1, month1, day1, i+1)
                resultlist = []
                # print("yaer", year)
                # print("month", month)
                # print("day", day)
                # print("hour", hour)
                # print(resource)
                # print(metric)
                filter1 = bytes(
                    "SingleColumnValueFilter ('Metric', 'resourceName', =, 'binary:{resource}') AND SingleColumnValueFilter ('Metric', 'index_name', =, 'binary:{metric}') AND SingleColumnValueFilter ('Metric', 'type', =, 'binary:pod')AND SingleColumnValueFilter ('Metric', 'namespace_name', =, 'binary:{namespace}')".format(
                        resource=resource, namespace=namespace, metric=metric, year=year, month=month, hour=hour),
                    encoding='utf-8')
                result = t.scan(filter=filter1, row_prefix=bytes(
                    '{year}-{month}-{day}T{hour}'.format(year=year, month=month, day=day, hour=hour), encoding='utf-8'))
                for k, v in result:
                    # print(k, v)
                    resultlist.append(float(v[b'Metric:index_value'].decode()))
                result_list.append(resultlist)
        else:
            for i in range(pretime):
                year, month, day = self.time_handle(year1, month1, day1, i)
                resultlist = []
                # print("yaer",year)
                # print("month",month)
                # print("day",day)
                # print("hour",hour)
                # print(resource)
                # print(metric)
                filter1 = bytes(
                    "SingleColumnValueFilter ('Metric', 'resourceName', =, 'binary:{resource}') AND SingleColumnValueFilter ('Metric', 'index_name', =, 'binary:{metric}') AND SingleColumnValueFilter ('Metric', 'time', =, 'regexstring:{year}-{month}-.*T{hour}:.*:.*') AND SingleColumnValueFilter ('Metric', 'type', =, 'binary:node')".format(
                        resource=resource, metric=metric, year=year, month=month, hour=hour), encoding='utf-8')
                result = t.scan(filter=filter1, row_prefix=bytes(
                    '{year}-{month}-{day}T{hour}'.format(year=year, month=month, day=day, hour=hour), encoding='utf-8'))
                for k, v in result:
                    # print(k, v)
                    resultlist.append(float(v[b'Metric:index_value'].decode()))
                result_list.append(resultlist)
        for i in range(pretime):
            # print(result_list[i])
            return_list = return_list + result_list[i]
        # t = connection.table('Monitor_record')
        # return_list = []
        # result_list = []
        #
        # if namespace:
        #     for i in range(pretime):
        #         year, month, day = self.time_handle(year, month, day, 1)
        #         resultlist = []
        #         print("yaer",year)
        #         print("month",month)
        #         print("day",day)
        #         print("hour",hour)
        #         print(resource)
        #         print(metric)
        #         print(pretime)
        #         filter1 = bytes(
        #             "SingleColumnValueFilter ('Metric', 'resourceName', =, 'binary:{resource}') AND SingleColumnValueFilter ('Metric', 'index_name', =, 'binary:{metric}') AND SingleColumnValueFilter ('Metric', 'type', =, 'binary:pod')AND SingleColumnValueFilter ('Metric', 'namespace_name', =, 'binary:{namespace}')".format(
        #                 resource=resource,namespace=namespace, metric=metric, year=year, month=month, hour=hour), encoding='utf-8')
        #         result = t.scan(filter=filter1, row_prefix=bytes(
        #             '{year}-{month}-{day}T{hour}'.format(year=year, month=month, day=day, hour=hour), encoding='utf-8'))
        #         for k, v in result:
        #             print(k, v)
        #             resultlist.append(float(v[b'Metric:index_value'].decode()))
        #         result_list.append(resultlist)
        # else:
        #     for i in range(pretime):
        #         year, month, day = self.time_handle(year, month, day, 1)
        #         resultlist = []
        #         print("year",year)
        #         print("month",month)
        #         print("day",day)
        #         print("hour",hour)
        #         print(resource)
        #         print(metric)
        #         filter1 = bytes(
        #             "SingleColumnValueFilter ('Metric', 'resourceName', =, 'binary:{resource}') AND SingleColumnValueFilter ('Metric', 'index_name', =, 'binary:{metric}') AND SingleColumnValueFilter ('Metric', 'time', =, 'regexstring:{year}-{month}-.*T{hour}:.*:.*') AND SingleColumnValueFilter ('Metric', 'type', =, 'binary:node')".format(
        #                 resource=resource, metric=metric, year=year, month=month, hour=hour), encoding='utf-8')
        #         result = t.scan(filter=filter1, row_prefix=bytes(
        #             '{year}-{month}-{day}T{hour}'.format(year=year, month=month, day=day, hour=hour), encoding='utf-8'))
        #         for k, v in result:
        #             print(k, v)
        #             resultlist.append(float(v[b'Metric:index_value'].decode()))
        #         result_list.append(resultlist)
        # for i in range(pretime):
        #     # print(result_list[i])
        #     return_list = return_list + result_list[i]



        return return_list


    def time_handle(self,year, month, day,pretime):
        year = int(year)
        month = int(month)
        day = int(day)

        if (day > pretime):
            day = day - pretime

        else:
            if (month > 1):
                month = month - 1
                if (month in [1, 3, 5, 7, 8, 10, 12]):
                    day = 31+day-pretime
                elif (month in [4, 6, 9, 11]):
                    day = 30+day-pretime
                elif year % 400 == 0 or year % 4 == 0 and year % 100 != 0:
                    day = 29+day-pretime
                else:
                    day = 28+day-pretime
            else:
                year = year - 1
                month = 12
                day = 31+day-pretime
        if (month >= 10):
            month = str(month)
        else:
            month = '0' + month
        if (day >= 10):
            day = str(day)
        else:
            day = '0' + str(day)
        year=str(year)
        return year, month, day

    def this_time(self):
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d-%H-M')
        return date
    def time_transfor(self,year, month, day, hour):
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        hour = hour + 8
        if hour > 24:
            hour = hour - 24
            day = day + 1
        if month in [1, 3, 5, 7, 8, 10, 12]:
            if day == 32:
                day = 1
                month = month + 1
        elif month in [4, 6, 9, 11]:
            if day == 31:
                day = 1
                month = month + 1
        elif year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            if day == 30:
                day = 1
                month = month + 1
        else:
            if day == 29:
                day = 1
                month = month + 1
        if month == 13:
            month = 1
            year = year + 1
        return year, month, day, hour
    def send(self,message):
        producer = self.producer
        # 调用send方法，发送名字为'ai_threshold_alert'的topicid ，发送的消息为message_string
        # response = producer.send('ai_threshold_alert', message)
        response = producer.send(self.producer_topic, message)
        producer.flush()

    def time_out_judge(self,time1,time2):
        #time1是现在时，time2是历史UTC时
        year1,month1,day1,hour1=self.time_handle_now(time1)
        year2,month2,day2,hour2=self.time_handle_now(time2)
        year1=int(year1)
        year2=int(year2)
        month1=int(month1)
        month2=int(month2)
        day1=int(day1)
        day2=int(day2)
        hour1=int(hour1)
        hour2=int(hour2)
        #False未过期 True过期了
        t1 = datetime.datetime(year1, month1, day1, hour1)
        t2 = datetime.datetime(year2, month2, day2, hour2)
        if((t1-t2).days>=1):

            return True
        else :
            return False
    def exist_judge(self,time1):
        # year1,month1,day1,hour1=self.time_handle_now(time1)
        # year1,month1,day1,hour1=self.time_transfor(year1,month1,day1,hour1)
        # t1=datetime.datetime.now()
        # t2=datetime.datetime(int(year1),int(month1),int(day1),int(hour1))
        t1=time1
        t2=time.time()
        t1=datetime.datetime.fromtimestamp(t1)
        t2=datetime.datetime.fromtimestamp(t2)
        if (t2-t1).seconds>=300:
            return True
        else :
            return False
    def consumer_metric(self):
        # 消费topic1的topic，并指定group_id(自定义)，多个机器或进程想顺序消费，可以指定同一个group_id，
        # 如果想一条消费多次消费，可以换一个group_id,会从头开始消费
        consumer = self.consumer
        print("=======开始消费==========")
        for message in consumer:
            # json读取kafka的消息
            # print(message.value)
            content = json.loads(message.value)
            # print(content)
            # print(type(content))
            # content=message.value.decode()
            # print(content)
            # print(type(content))
            # content = eval(content)
            # print(type(content))
            # print(content)
            # for i in content:
            #     print(i)
            #     print(i["deviceName"])
            #     print(i["time"])
            #     print(i["metric"])
            #     print(type(i["metric"]))
            #     print(i["value"])
            #     print(i["range"])
            #     print(i["result"])
            for i in content:
                    # print(content)
                    # print(i)
                    # print(type(i))
                    #非空判断
                    # 这里注意要字符串转float
                    #还得注意是否存在这个属性

                    # TODO 其他指标待添加
                    if 'name'in i.keys():
                        name = i['name']
                    else:
                        continue
                    timeinfo = i['time']
                    low=0
                    hign=0
                    # 与内存中结果作对比，内存中找不到去每天存一份的日志找，日志中找不到就去数据库查？
                    #flag过期或没有则为TRUE
                    cpu_flag=True
                    memory_flag=True
                    if name in self.data.keys():
                        print(name)
                        # 2018-10-06T06:10:11Z
                        year, month, day, hour = self.time_handle_now(timeinfo)
                        #同一天false，不同天true
                        memory_usage = 0
                        if "memory/usage" in i.keys():
                            memory_usage = float(i['memory/usage'])
                            if "memory/usage" in self.data[name].keys():
                                if "timeout" in self.data[name]["memory/usage"].keys():
                                    memory_flag = self.time_out_judge(timeinfo, self.data[name]["memory/usage"]["timeout"])
                                if memory_flag:
                                    # TODO 这里目前只存了memory/usage和cpu/usage_rate
                                    self.data[name]["memory/usage"]["timeout"] = timeinfo
                                    names = name.split("_")
                                    namespace = 0
                                    if len(names) == 4:
                                        namespace = names[-2]
                                    print(names, namespace, year, month, day, hour, self.data, self.data[name])
                                    memory_usage_list = self.select("memory/usage", name.split("_")[-1], namespace,
                                                                    year, month, day, hour,
                                                                    self.data[name]["memory/usage"]["sampleDataTimeRange"])
                                    hign = 0
                                    low = 0
                                    if memory_usage_list:
                                        hign, low = self.NDtest(memory_usage_list)
                                    self.data[name]["memory/usage"]["memory_usage_hign"] = hign
                                    self.data[name]["memory/usage"]["memory_usage_low"] = low
                                self.data[name]["memory/usage"]["latestTime"] = time.time()
                                self.data[name]["memory/usage"]["time"] = timeinfo
                                self.decide(name, "memory/usage", memory_usage, self.data[name]["memory/usage"]["memory_usage_low"],
                                            self.data[name]["memory/usage"]["memory_usage_hign"],self.data[name]["memory/usage"]["ruleId"], timeinfo)
                        cpu_usage_rate =0
                        if "cpu/usage_rate" in i.keys():
                            cpu_usage_rate = float(i['cpu/usage_rate'])
                            if  "cpu/usage_rate" in self.data[name].keys():
                                if "timeout" in self.data[name]["cpu/usage_rate"].keys():
                                    cpu_flag = self.time_out_judge(timeinfo, self.data[name]["cpu/usage_rate"]["timeout"])
                                if cpu_flag:
                                    self.data[name]["cpu/usage_rate"]["timeout"] = timeinfo
                                    names = name.split("_")
                                    namespace = 0
                                    if len(names) == 4:
                                        namespace = names[-2]
                                    print(names, namespace, year, month, day, hour, self.data, self.data[name])
                                    cpu_usage_rate_list = self.select("cpu/usage_rate", name.split("_")[-1], namespace,
                                                                      year,
                                                                      month, day, hour,
                                                                      self.data[name]["cpu/usage_rate"][
                                                                          "sampleDataTimeRange"])
                                    # TODO 取数据
                                    hign = 0
                                    low = 0
                                    if cpu_usage_rate_list:
                                        hign, low = self.NDtest(cpu_usage_rate_list)
                                        if low < 0:
                                            low = 0
                                    self.data[name]["cpu/usage_rate"]["cpu_usage_rate_hign"] = hign
                                    self.data[name]["cpu/usage_rate"]["cpu_usage_rate_low"] = low
                                self.data[name]["cpu/usage_rate"]["latestTime"] = time.time()
                                self.data[name]["cpu/usage_rate"]["time"] = timeinfo
                                self.decide(name, "cpu/usage_rate", cpu_usage_rate,
                                            self.data[name]["cpu/usage_rate"]["cpu_usage_rate_low"],
                                            self.data[name]["cpu/usage_rate"]["cpu_usage_rate_hign"],self.data[name]["cpu/usage_rate"]["ruleId"], timeinfo)
            #有数据过来才能催动这个循环,而且如果创建后没来过的话没有time的，还得处理
            for name in data.keys():
                for metric in data[name].keys():
                    if metric=="cpu/usage_rate":
                        if self.exist_judge(data[name]["cpu/usage_rate"]["latestTime"]):
                            self.decide(name, "cpu/usage_rate", 0, 0,
                                        0, self.data[name]["cpu/usage_rate"]["ruleId"],"")

                    if metric=="memory/usage":
                        if self.exist_judge(data[name]["memory/usage"]["latestTime"]):
                            self.decide(name, "memory/usage", 0, 0,
                                        0, self.data[name]["memory/usage"]["ruleId"],"")
    def time_out(self,time1,time2):
        hour1=int(time1[12:14])
        hour2=int(time2[12:14])
        minute1=int(time1[15:17])
        minute2=int(time2[15:17])
        second1=int(time1[18:20])
        second2=int(time2[18:20])
    def time_handle_pre(self,timeinfo):
        year=int(timeinfo[0:4])
        month = int(timeinfo[5:7])
        hour = timeinfo[11:13]
        if(month>1):
            if(month>10):
                month=month-1
                month=str(month)
            else:
                month=month-1
                month='0'+str(month)
        else:
            month='12'
            year=year-1
            year=str(year)
        return year,month,hour
    def time_handle_now(self,timeinfo):
        year=timeinfo[0:4]
        month = timeinfo[5:7]
        day=timeinfo[8:10]
        hour = timeinfo[11:13]
        return year,month,day,hour

    def decide(self,name,metric_str,metric_value,low,hign,ruleId,timeinfo):
        message = {}


        #为0就算异常

        if metric_value==0 :
            message["result"]="zero"
        elif low==0 and hign==0:
            message["result"] ="empty"

        elif metric_value > hign:
             print("hign", name, metric_str, metric_value, low, hign)
             message["result"] = "high"
        elif metric_value < low:
             print("low", name, metric_str, metric_value, low, hign)
             message["result"] = "low"
        else:
            return
        message["deviceName"] = name
        message["metric"] = metric_str
        message["time"] = timeinfo
        message["value"] = str(metric_value)
        message["range"] = [low, hign]
        message["ruleId"]=ruleId
        #这里在初始化里已经json化了
        # message = json.dumps(message)
        self.send(message)

    def NDtest(self,value_list):
        # 正态性检验
        XX = np.array(value_list)
        m=XX.mean()
        s=XX.std()
        #这里要大于等于或小于等于，防止常数时列表为空
        value_list=[x for x in value_list if x>=m-3*s and x<=m+3*s]
        # X_scaled = preprocessing.scale(XX)
        # print(X_scaled.mean())
        # print(kstest(X_scaled,'norm'))
        # print(normaltest(X_scaled))
        p = np.array(value_list)
        # print(len(p))
        mu = np.mean(p)
        sigma = np.std(p)
        #万一是常数列，那么方差为0，不能作除法
        if sigma==0:
            return mu,mu
        med = np.median(p)
        # print(mu)
        # print(sigma)
        # 偏度系数sk，衡量正太分布的偏态程度
        sk = (mu - med) / sigma
        # print(sk)
        # 记录是否取过对数
        flag = 0
        # 偏度系数太大，考虑偏态分布，对数正太分布
        if -1 > sk or sk > 1:
            p = np.log2(p)
            flag = 1

        mu = np.mean(p)
        sigma = np.std(p)
        # 3sigma准则？

        # 标准化,似乎不用了，阈值直接公式算一下
        # p=(p-mu)/sigma
        # mu = np.mean(p)
        # sigma = np.std(p)
        # print(p)
        # print(mu)
        # print(sigma)
        hign = 1.96 * sigma + mu
        low = -1.96 * sigma + mu
        if flag == 1:
            hign = pow(2, hign)
            low = pow(2, low)

        # 阈值   正负1.96*sigma+mu
        # print("高阈值", hign)
        # print("低阈值", low)
        return hign, low

