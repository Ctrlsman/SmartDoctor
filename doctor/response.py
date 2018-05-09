# -*- coding：utf-8 -*-
import datetime
import json

from flask import Response
from doctor.utils.weixin import init_wechat_sdk


class ResponseEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, bytes):
            return o.decode('utf-8')

        return json.JSONEncoder.default(self, o)


class JsonResponse:
    def __init__(self, data):
        code = 0
        msg = 'ok'
        if isinstance(data, dict):
            code = data.pop('code', 0)
            msg = data.pop('msg', '')

        self.data = {
            'code': code,
            'msg': msg,
        }

        if data is not None:
            self.data['data'] = data

    def to_response(self):
        return Response(
            response=json.dumps(self.data, cls=ResponseEncoder),
            status=200,
            mimetype='application/json'
        )


# 储存微信消息类型所对应函数（方法）的字典
msg_type_resp = {}


def set_msg_type(msg_type):
    """
    储存微信消息类型所对应函数（方法）的装饰器
    """
    def decorator(func):
        msg_type_resp[msg_type] = func
        return func
    return decorator


@set_msg_type('text')
def text_resp():
    """文本类型回复"""
    # 默认回复微信消息
    response = 'success'
    return response


def wechat_response(data):
    """微信消息处理回复"""
    global message, openid, wechat

    wechat = init_wechat_sdk()
    wechat.parse_data(data)
    message = wechat.get_message()
    openid = message.source
    # 用户信息写入数据库
    # set_user_info(openid)

    try:
        get_resp_func = msg_type_resp[message.type]
        response = get_resp_func()
    except KeyError:
        # 默认回复微信消息
        response = 'success'

    # 保存最后一次交互的时间
    # set_user_last_interact_time(openid, message.time)
    return response