from flask import Flask
from flask import request
import hashlib
from lxml.etree import parse


app = Flask(__name__)


@app.route('/')
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
    if request.method == 'POST':
        str_xml = request.data  # 获得post来的数据
        xml = lxml.fromstring(str_xml)  # 进行XML解析
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        if msgType == 'text':
            content = xml.find("Content").text
            return self.render.reply_text(fromUser, toUser, int(time.time()), content)
        elif msgType == 'image':
            pass
        else:
            pass


if __name__ == '__main__':
    app.run(port=8099)
