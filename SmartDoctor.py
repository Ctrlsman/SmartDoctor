from flask import Flask
from flask import request

import hashlib
from xml.etree import ElementTree as ET
import time

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def check():
    token = 'wodexiangmu'
    req_data = request.args
    signature = req_data.get("signature")
    timestamp = req_data.get("timestamp")
    nonce = req_data.get("nonce")
    echostr = req_data.get("echostr")
    l = [token, timestamp, nonce]
    l.sort()
    s = l[0] + l[1] + l[2]
    hashcode = hashlib.sha1(s.encode()).hexdigest()
    if hashcode == signature:
        return echostr
    if request.data:
        xml = ET.fromstring(request.data)
        me = xml.find("ToUserName").text
        user = xml.find("FromUserName").text
        postTime = str(int(time.time()))
        msgType = xml.find("MsgType").text
        if msgType == 'event':
            e = xml.find('Event').text
            if e == 'subscribe':
                return '欢迎光临，非常高兴能为您服务！回复h开始尽享方便快捷生活吧~'
            elif e == 'unsubscribe':
                return '非常荣幸能为您服务！下次再见～'
        # msgid check. if repeat, reponse with ""
        msgid = xml.find("MsgId").text
        return '111'


if __name__ == '__main__':
    app.run(port=8099)
