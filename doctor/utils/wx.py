import datetime
import time
from urllib.parse import urlencode
import hashlib
import logging

import requests

from consumer import config
from consumer.models.base import redis_pool_get
from consumer.thirdparty.wx.utils import xml2dict, dict2xml, gen_nonce_str
from consumer import exceptions

MCH_ID = config.WX_MCH_ID
MCH_SECRET = config.WX_MCH_SECRET

APP_ID = config.WX_APP_ID
APP_SECRET = config.WX_APP_SECRET

PAY_URL = config.WX_PAY_URL
API_URL = config.WX_API_URL
NOTIFY_URL = config.PAY_NOTIFY_URL

logger = logging.getLogger(__name__)


def sign(data):
    key = MCH_SECRET
    non_empty_keys = filter(lambda k: data[k], data.keys())
    sorted_keys = sorted(non_empty_keys)
    str_sign_temp = '&'.join('{}={}'.format(k, data[k]) for k in sorted_keys) + '&key=' + key
    return hashlib.md5(str_sign_temp.encode('utf-8')).hexdigest().upper()


def unified_order(order_no, amount, open_id):
    now = datetime.datetime.now()
    time_start = now.strftime('%Y%m%d%H%M%S')
    time_expire = (now + datetime.timedelta(minutes=3)).strftime('%Y%m%d%H%M%S')
    nonce_str = gen_nonce_str()

    if amount <= 0:
        raise exceptions.ParamsErr

    req_data = {
        'appid': APP_ID,
        'mch_id': MCH_ID,
        'nonce_str': nonce_str,
        'body': '洗车-消费',
        'out_trade_no': order_no,
        'total_fee': amount,
        'time_start': time_start,
        'time_expire': time_expire,
        'spbill_create_ip': '101.201.148.24',
        'notify_url': NOTIFY_URL,
        'trade_type': 'JSAPI',
        'openid': open_id
    }

    signature = sign(req_data)
    req_data['sign'] = signature

    req_data = dict2xml('xml', req_data)
    resp = requests.post(PAY_URL + '/pay/unifiedorder', data=req_data)
    resp_data = xml2dict(resp.content)
    return resp_data


def again_sign(prepay_id):
    sign_data = {
        'appId': APP_ID,
        'nonceStr': gen_nonce_str(),
        'package': 'prepay_id={}'.format(prepay_id),
        'signType': 'MD5',
        'timeStamp': str(int(time.time()))
    }
    signature = sign(sign_data)
    sign_data['paySign'] = signature
    return sign_data


def get_sign_key():
    req_data = {
        'mch_id': MCH_ID,
        'nonce_str': gen_nonce_str(),
    }
    signature = sign(req_data)
    req_data['sign'] = signature

    req_data = dict2xml('xml', req_data)
    resp = requests.post(PAY_URL + '/pay/getsignkey', data=req_data)
    resp_data = xml2dict(resp.content)
    return resp_data['sandbox_signkey']


def get_access_token():
    cache = redis_pool_get()
    wx_access_token = cache.get('wx_access_token')
    if wx_access_token:
        return wx_access_token

    data = {
        'grant_type': 'client_credential',
        'appid': APP_ID,
        'secret': APP_SECRET,
    }
    url = API_URL + '/cgi-bin/token?' + urlencode(data)
    resp = requests.get(url)
    resp_json = resp.json()
    access_token = resp_json['access_token']
    expires_in = resp_json['expires_in'] - 10

    cache.set('wx_access_token', access_token, expires_in)
    return access_token


def notify(open_id, tmpl_id, form_id, tmpl_data, page=None):
    data = {
        'touser': open_id,
        'template_id': tmpl_id,
        'form_id': form_id,
        'data': tmpl_data,
    }
    if page:
        data['page'] = page

    url = API_URL + '/cgi-bin/message/wxopen/template/send?access_token=' + get_access_token()
    resp = requests.post(url, json=data)
    logger.debug(resp.text)
    if resp.status_code == 200:
        resp_json = resp.json()
        logger.debug('notify resp:', resp_json)
        if resp_json['errcode'] == 0:
            return True
    return False
