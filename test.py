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


class Activation:
    def __init__(self):
        print("init")  # never prints
        self.answer_topic = "$xlink/device/activation/result"
        self.device_topic = "$xlink/device/activation"
        self.pid = "160002baec9203e9160002baec92c601"
        self.pkey = "7c74dc459c1b55926184df2f3bd29d65"
        self.client_id1 = "X:DEVICE;A:2;V:1;"

    def activation_device(self):
        client_id1 = "X:DEVICE;A:2;V:1;"
        message1 = json.dumps({"product_id": self.pid, "mac": "AAA1"})
        password1 = (encrypt_md5(self.pid + self.pkey))
        mess = Mqtt_subscribe(self.answer_topic, client_id1, self.pid, password1)
        mess.start()
        mqtt_Publish(self.device_topic, message1, self.pid, password1)


if __name__ == '__main__':
    a = Activation()
    a.activation_device()