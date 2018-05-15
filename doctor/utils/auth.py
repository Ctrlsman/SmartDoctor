# -*- coding：utf-8 -*-
import requests
from doctor import config
from doctor.models.base import redis_pool_get


class WXAuthApi:
    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def get_access_token(self):
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



