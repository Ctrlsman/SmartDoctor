# -*- coding：utf-8 -*-
import redis
import config


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