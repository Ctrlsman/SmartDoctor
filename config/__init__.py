# -*- coding：utf-8 -*-
import os

ENV = os.environ.get('DOCTOR', 'dev')

HTTP_HOST = '127.0.0.1'
HTTP_PORT = 8989

SQLALCHEMY_TRACK_MODIFICATIONS = False

if ENV == 'dev':
    from config.dev import *
else:
    from config.prd import *

try:
    from config.local import *
except ImportError:
    pass