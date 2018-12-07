# @Time   : 2018-10-23
# @Author : zxh
from zutils.zrpc.server.threadpool_server import ThreadpoolServer, map_handle
from zutils.logger import Logger
import time
import datetime
import math
import happybase
import numpy as np
import json
from kafka import *
import configparser
import threading
from myclass import MyClass
from myclass import data
#阈值告警
# 创建服务，单例，如果资源有竞争，创建放在func里
#
# def this_time():
#     now = datetime.datetime.now()
#     date = now.strftime('%Y-%m-%d-%H-%M')
#     return date

@map_handle('/add', 'handle1', 10)
@map_handle('/delete', 'handle2', 10)
@map_handle('/modify', 'handle3', 10)
@map_handle('/select', 'handle4', 10)
class ExampleSvr():
        #新增某些处理节点
    def handle1(self, task):
        print(task)
        record=task
        # record=task
        i=task
        ruleId=i["ruleId"]
        metricName=i["metricName"]
        deviceName=i["deviceName"]
        sampleDataTimeRange=i["sampleDataTimeRange"]
        if deviceName in data.keys():
            data[deviceName][metricName]={}
            data[deviceName][metricName]["sampleDataTimeRange"]=sampleDataTimeRange[:-1]
            data[deviceName][metricName]["latestTime"]=time.time()
            data[deviceName][metricName]["ruleId"] = i["ruleId"]
        else:
            data[deviceName]={}
            data[deviceName][metricName] = {}
            data[deviceName][metricName]["sampleDataTimeRange"] = sampleDataTimeRange[:-1]
            data[deviceName][metricName]["latestTime"] = time.time()
            data[deviceName][metricName]["ruleId"] = i["ruleId"]
        print(data)
        return data
        #删除某些容器节点
    def handle2(self,task):
        # record=task

        record=task
        ruleId=record["ruleId"]
        metricName=record["metricName"]
        deviceName=record["deviceName"]
        for name in data.keys():
            if name==deviceName:
                if data[name][metricName]["ruleId"]==ruleId:
                    del data[name][metricName]

                else: raise Exception("not matched")
        k=data.keys()
        for name in list(k):
            if not data[name].keys():
                del data[name]
        return data
        #修改时间
    def handle3(self, task):
        #TODO 时间更改要作变更
        record=task
        ruleId=record["ruleId"]
        metricName=record["metricName"]
        deviceName=record["deviceName"]
        sampleDataTimeRange=record["sampleDataTimeRange"]
        sampleDataTimeRange=sampleDataTimeRange[:-1]
        data[deviceName][metricName]["ruleId"]=ruleId
        data[deviceName][metricName]["sampleDataTimeRange"]=sampleDataTimeRange
        data[deviceName][metricName]["lastestTime"]=time.time()
        del data[deviceName][metricName]["timeout"]

        return data
    def handle4(self, task):

        return data
print(12)
t=MyClass()
t.start()
print(11)
cf = configparser.ConfigParser()
cf.read("python.ini")
redis_server = cf.get("register", "address")
logger = Logger(Logger.INFO, 'example', True)
# 参数：日志级别   日志文件名   日志是否控制台输出

print(redis_server)
print(type(redis_server))
server = ThreadpoolServer(redis_server, [ExampleSvr], logger, 'JSON',30, 30,  1)
#          消息系统地址    服务列表     日志     交互协议    线程数量

server.start()




