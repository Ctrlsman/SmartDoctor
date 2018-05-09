# -*- coding：utf-8 -*-
from flask import Blueprint
from flask import request
from doctor.utils.weixin import check_signature
from doctor.response import wechat_response

bp = Blueprint('wx', __name__)


@bp.route("/", methods=['GET', 'POST'])
@check_signature
def handle_wechat_request():
    """
    处理回复微信请求
    """
    if request.method == 'POST':
        return wechat_response(request.data)
    else:
        # 微信接入验证
        return request.args.get('echostr', '')