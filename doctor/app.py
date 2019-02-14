# -*- coding：utf-8 -*-
import sys
import logging
import json
import traceback
from doctor import config
from doctor.log.handle import MidnightRotatingFileHandler
from doctor.response import JsonResponse
from doctor.models.base import db, redis_pool_connect
from doctor.exceptions.base import DoctorException
from flask import Flask
from flask import request
from werkzeug.utils import find_modules

logger = logging.getLogger(__name__)


def init_log():
    fmt = ("%(asctime)s %(levelname)s "
           "[%(name)s:%(lineno)d] %(message)s")

    if config.DEBUG:
        handler = logging.StreamHandler(sys.stdout)
    else:
        handler = MidnightRotatingFileHandler(config.LOG_PATH)

    logging.basicConfig(
        level=logging.DEBUG,
        format=fmt,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[handler]
    )

    logging.getLogger('werkzeug').setLevel(logging.WARNING)


class DoctorFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, (dict, list)):
            rv = JsonResponse(rv)
            return rv.to_response()
        return Flask.make_response(self, rv)


def register_blueprints(app, path):
    def _import_string(import_name):
        import sys
        import_name = str(import_name).replace(':', '.')
        try:
            __import__(import_name)
        except ImportError:
            raise
        else:
            return sys.modules[import_name]

    for name in find_modules(path):
        mod = _import_string(name)
        if not hasattr(mod, 'bp'):
            continue
        urls = name.split('.')
        prefix = '/{}'.format(urls[-1])
        app.register_blueprint(mod.bp, url_prefix=prefix)


def register_after_request(app):
    @app.after_request
    def log_response(resp):
        log_msg = {
            'url': request.path,
        }
        try:
            req_json_data = request.get_json()
            if req_json_data:
                log_msg['req_data'] = req_json_data
        except:
            pass

        try:
            resp_json_data = json.loads(resp.data)
            log_msg['resp_data'] = resp_json_data
        except:
            pass
        if config.DEBUG:
            log_msg = json.dumps(log_msg, indent=2, ensure_ascii=False)

        logger.debug(log_msg)
        return resp

    @app.after_request
    def close_db_session(resp):
        try:
            db.session.remove()
        except:
            pass
        return resp


def register_err_handler(app):
    @app.errorhandler(DoctorException)
    def handle_api_err(err):
        logger.error(traceback.format_exc())
        return err.to_result()

    @app.errorhandler(Exception)
    def handle_exception(err):
        logger.error(traceback.format_exc())
        err = DoctorException()
        return err.to_result()


def create_app():
    init_log()

    app = DoctorFlask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    register_blueprints(app, 'doctor.views')
    register_after_request(app)
    register_err_handler(app)

    return app
