import redis
from fastapi import Depends
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache(expire=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            result = redis_client.get(key)
            if result:
                return result
            result = await func(*args, **kwargs)
            redis_client.setex(key, expire, result)
            return result
        return wrapper
    return decorator
