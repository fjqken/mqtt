import paho.mqtt.client as mqtt
import threading
import time
import ast
from hashlib import md5

HOST = "mqtt.xlink.cn"
PORT = 1883


def encrypt_md5(s):
    # 创建md5对象
    new_md5 = md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()


class Mqtt_subscribe(threading.Thread):
    """
    mqtt订阅
    """

    def __init__(self, subtopic, client_id1, username1, password1):
        super(Mqtt_subscribe, self).__init__()
        self.client_id = client_id1
        self.client = mqtt.Client(self.client_id)
        self.client.user_data_set(subtopic)  # topic
        self.client.username_pw_set(username1, password1)
        self.tid = None
        self.macaddress = None
        self.type = None
        self.status = None
        self.subtype = None
        self.info = None
        self.answer_result = None

    def run(self):
        # ClientId不能重复，所以使用当前时间
        # 必须设置，否则会返回「Connected with result code 4」
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(HOST, PORT, 60)
        self.client.loop_forever(timeout=10)

    def on_connect(self, client, subtopic, flags, rc):
        print("Connected with result code " + str(rc))
        print("topic:" + subtopic)
        client.subscribe(subtopic, 2)

    def on_message(self, client, userdata, msg):
        # print(msg.topic + " " + msg.payload.decode("utf-8"))
        mess = msg.payload.decode("utf-8")
        print(mess)
        # 在此处处理订阅主题返回的信息
        user_dict = ast.literal_eval(mess)
        self.answer_result = user_dict
        self.tid = user_dict['tid']
        self.macaddress = user_dict['macaddr']
        try:
            self.type = user_dict['type']
        except BaseException:
            pass
        try:
            self.subtype = user_dict['subtype']
        except BaseException:
            pass
        try:
            self.info = user_dict['info']
        except BaseException:
            pass
        try:
            self.status = user_dict['status']
        except BaseException:
            pass
        if self.macaddress and self.tid:
            self.client.disconnect()
            # print('macaddress:',self.macaddress)
            # print('tid:', self.tid)

        return self.macaddress, self.tid, self.status, self.type, self.info, self.subtype


if __name__ == "__main__":
    subtopic = "$xlink/device/activation"
    client_id1 = "X:DEVICE;A:2;V:1;"
    pid = "160002baec9203e9160002baec92c601"
    pkey = "7c74dc459c1b55926184df2f3bd29d65"
    print(pid+pkey)
    password1 = (encrypt_md5(pid+pkey))
    print(password1)
    print(client_id1)
    t = Mqtt_subscribe(subtopic, client_id1, pid, password1)
    a = t.client
    t.start()
