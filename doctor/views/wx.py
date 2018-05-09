# -*- coding：utf-8 -*-
from flask import Blueprint
from flask import request
from flask import make_response
import xml.etree.ElementTree as ET
from doctor.utils.weixin import check_signature
from doctor.response import wechat_response
import time

bp = Blueprint('/wx', __name__)


@bp.route('/', methods=['GET', 'POST'])
@check_signature
def handle_wechat_request():
    """
    处理回复微信请求
    """
    if request.method == 'POST':
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(reply % (FromUserName, ToUserName, str(int(time.time())), Content))
        response.content_type = 'application/xml'
        return response
    else:
        # 微信接入验证
        return request.args.get('echostr', '')