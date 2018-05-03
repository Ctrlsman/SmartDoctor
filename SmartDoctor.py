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
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        return echostr


if __name__ == '__main__':
    app.run()
