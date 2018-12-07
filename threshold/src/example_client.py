# @Time   : 2018-10-24
# @Author : zxh


# 测试
import requests
import  json


# r = requests.get('http://192.168.213.51:8899/test1')
#
# print(r.json())
# ,"default_k8s-alpha-node1_0pk2uk_d123-7768b46578-vm78b"
# payload=["default_k8s-alpha-node1_default_kafka-2","default_k8s-alpha-node1_default_kafka-1","default_k8s-alpha-node1","default_k8s-alpha-node2","default_k8s-alpha-node2_0pk2uk_d123-7768b46578-nc6hl"]
# payload={"data":payload}
# payload={
# 	"ruleId": "24ed9e94-2f19-462f-bff9-3ab9b42f8d70",
# 	"metricName": "memory/usage",
# 	"deviceName": "default_k8s-alpha-node1_container-platform-5d57c84597-ccqr4",
# 	"sampleDataTimeRange": "7"
# }
# payload={
# 	"ruleId": "24ed9e94-2f19-462f-bff9-3ab9b4luanlaide",
# 	"metricName": "memory/usage",
# 	"deviceName": "default_k8s-alpha-node1",
# 	"sampleDataTimeRange": "7d"
# }
payload={
	"ruleId": "24ed9e94-2f19-462f-bff9-3ab9b4luanlaidaae",
	"metricName": "memory/usage",
	"deviceName": "default_k8s-alpha-node1_default_kafka-2",
	"sampleDataTimeRange": "1d"
}
# payload={'ruleId': '24ed9e94-2f19-462f-bff9-3ab9b42f8d70', 'deviceName': 'default_k8s-alpha-node1_default_container-platform-84cb4cd749-ms59n', 'metricName': 'memory/usage', 'sampleDataTimeRange': '7d'}
# payload={
#    "ruleId": "24ed9e94-2f19-462f-bff9-3ab9b42f8d70",
#    "metricName": "memory/usage",
#    "deviceName": "default_k8s-alpha-node1",
#    "sampleDataTimeRange": "3"
# }
r = requests.post('http://192.168.213.51:8899/add', json=payload)
# r = requests.post('http://192.168.1.111:8899/add', json=payload)
# payload={"data":["default_k8s-alpha-node1","default_k8s-alpha-node2"]}
# r = requests.post('http://192.168.213.51:8899/delete', json=payload)
# r=requests.get('http://192.168.213.51:8899/select')
# r=requests.get('http://192.168.1.111:8899/select')


# payload={"time":15}
# r = requests.post('http://192.168.213.51:8899/modify', json=payload)
print(r.json())
# a={"a":"a","b":"b"}
# r=requests.get('http://192.168.213.51:8899/add',data=payload)

# r = requests.get('http://192.168.213.51:8899/add?data='+json.dumps(payload))
# def time_transfor(year,month,day,hour):
#     year=int(year)
#     month=int(month)
#     day=int(day)
#     hour=int(hour)
#     hour=hour+8
#     if hour>24:
#         hour=hour-24
#         day=day+1
#     if month in [1,3,5,7,8,10,12]:
#         if day==32:
#             day=1
#             month=month+1
#     elif month in [4,6,9,11]:
#         if day==31:
#             day=1
#             month=month+1
#     elif year%400==0 or (year%4==0 and year%100!=0):
#         if day==30:
#             day=1
#             month=month+1
#     else:
#         if day==29:
#             day=1
#             month=month+1
#     if month==13:
#         month=1
#         year=year+1
#     return year,month,day,hour
#
# import datetime
# year="2018"
# month="11"
# day="09"
# hour="10"
# t1=datetime.datetime.now()
# print(t1)
# year,month,day,hour=time_transfor(year,month,day,hour)
# t2=datetime.datetime(year,month,day,hour)
# if(t2-t1>1):
#
# print((t2-t1).days)

# t1=datetime.datetime(year1,month1,day1,hour1)
# t2=datetime.datetime(year2,month2,day2,hour2)

