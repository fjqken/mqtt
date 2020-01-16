import paho.mqtt.publish as publish
import time
from hashlib import md5
import json


def mqtt_Publish(topic, msg, username, password):
    client_id = "X:DEVICE;A:2;V:1;"
    IP_DNS = "mqtt.xlink.cn"
    port = 1883
    publish.single(topic, msg, qos=1,
                   hostname=IP_DNS,
                   port=port,
                   client_id=client_id,
                   auth={'username': username, 'password': password})


def encrypt_md5(s):
    # 创建md5对象
    new_md5 = md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()


if __name__ == '__main__':
    subtopic = "$1"
    client_id1 = "X:DEVICE;A:2;V:1;"
    pid = "160002baec9203e9160002baec92c601"
    pkey = "7c74dc459c1b55926184df2f3bd29d65"
    message1 = json.dumps({"Product ID": pid, "mac": "AAA1"})
    password1 = (encrypt_md5(pid + pkey))
    mqtt_Publish(subtopic, message1, pid, pkey)
