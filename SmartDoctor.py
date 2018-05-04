from flask import Flask
from flask import request
import hashlib

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
        return 111


if __name__ == '__main__':
    app.run(port=8099)
