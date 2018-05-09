# -*- coding：utf-8 -*-
from functools import wraps

from doctor import config

import requests
from flask import request, redirect
from flask import current_app
from wechat_sdk import WechatBasic
from doctor.models.base import redis_pool_get


def init_wechat_sdk():
    """初始化微信 SDK"""
    cache = redis_pool_get()
    access_token = cache.get("wechat:access_token")
    jsapi_ticket = cache.get("wechat:jsapi_ticket")
    token_expires_at = cache.get("wechat:access_token_expires_at")
    ticket_expires_at = cache.get("wechat:jsapi_ticket_expires_at")
    if access_token and jsapi_ticket and token_expires_at and ticket_expires_at:
        wechat = WechatBasic(appid=current_app.config['APP_ID'],
                             appsecret=current_app.config['APP_SECRET'],
                             token=current_app.config['TOKEN'],
                             access_token=access_token,
                             access_token_expires_at=int(token_expires_at),
                             jsapi_ticket=jsapi_ticket,
                             jsapi_ticket_expires_at=int(ticket_expires_at))
    else:
        wechat = WechatBasic(appid=current_app.config['APP_ID'],
                             appsecret=current_app.config['APP_SECRET'],
                             token=current_app.config['TOKEN'])
        access_token = wechat.get_access_token()
        cache.set("wechat:access_token", access_token['access_token'], 7000)
        cache.set("wechat:access_token_expires_at",
                  access_token['access_token_expires_at'], 7000)
        jsapi_ticket = wechat.get_jsapi_ticket()
        cache.set("wechat:jsapi_ticket", jsapi_ticket['jsapi_ticket'], 7000)
        cache.set("wechat:jsapi_ticket_expires_at",
                  jsapi_ticket['jsapi_ticket_expires_at'], 7000)

    return wechat


def check_signature(func):
    """
    微信签名验证
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')

        wechat = init_wechat_sdk()
        if not wechat.check_signature(signature=signature,
                                      timestamp=timestamp,
                                      nonce=nonce):
            if request.method == 'POST':
                return "signature failed"
            else:
                return redirect(current_app.config['MAIN_URL'])

        return func(*args, **kwargs)

    return decorated_function


def get_access_token():
    cache = redis_pool_get()
    wx_access_token = cache.get('wx_access_token')
    if wx_access_token:
        return wx_access_token

    data = {
        'grant_type': 'client_credential',
        'appid': config.APP_ID,
        'secret': config.APP_SECRET,
    }
    url = config.WX_API_URL + '/cgi-bin/token'
    resp = requests.get(url, params=data)
    resp_json = resp.json()
    access_token = resp_json['access_token']
    expires_in = resp_json['expires_in'] - 10

    cache.set('wx_access_token', access_token, expires_in)
    return access_token

