# -*- coding：utf-8 -*-
import re
import redis
import datetime
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import Column, BIGINT, DateTime
from sqlalchemy.ext.declarative import declared_attr
from doctor import config


class BaseModel(Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    @declared_attr
    def __tablename__(self):
        name = self.__name__
        return str(name[0]).lower() + re.sub(
            r'[A-Z]', lambda matched: '_' + str(matched.group(0)).lower(),
            name[1:])

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)

    def to_dict(self, fields=None):
        if not fields:
            fields = [x.name for x in self.__table__.columns]
        return {field: getattr(self, field) for field in fields}


db = SQLAlchemy(model_class=BaseModel)


_redis_pool = None


def redis_pool_connect():
    global _redis_pool
    _redis_pool = redis.ConnectionPool.from_url(
        config.REDIS_URL,
        config.REDIS_DB,
        charset='utf-8',
        decode_responses=True,
        decode_components=True,
    )


def redis_pool_get():
    global _redis_pool
    return redis.Redis(connection_pool=_redis_pool)