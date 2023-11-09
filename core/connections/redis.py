from aioredis import Redis


def get_redis_connection():
    return Redis()
