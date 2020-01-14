# import paho.mqtt.client as mqtt
#
# MQTTHOST ="mqtt.xlink.cn"
# MQTTPORT = 1883
#
# mqttclient = mqtt.Client()
#
# def on_connect():
#     mqttclient.connect(MQTTHOST,MQTTPORT,60)
#     mqttclient.loop_start()
#     print()
#
#
# on_connect()


import json
from mqtt_publish import mqtt_Publish
from time import sleep
from mqtt_subscribe import Mqtt_subscribe
from hashlib import md5
import datetime


def encrypt_md5(s):
    # 创建md5对象
    new_md5 = md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()


class Activation():
    def __init__(self):
        print("init")  # never prints

    pid = "160002baec9203e9160002baec92c601"

    def activation_device(self):
        subtopic = "$xlink/device/activation"
        client_id1 = "X:DEVICE;A:2;V:1;"
        pid = self.pid
        pkey = "7c74dc459c1b55926184df2f3bd29d65"
        message1 = json.dump({"product_id": pid, "mac": "AAA1" })
        print(pid + pkey)
        password1 = (encrypt_md5(pid + pkey))
        print(password1)
        print(client_id1)
        mess = Mqtt_subscribe(subtopic, client_id1, pid, password1)
        mess.start()
        mqtt_Publish(subtopic, message1, pid, pkey)


a =Activation()
a.activation_device