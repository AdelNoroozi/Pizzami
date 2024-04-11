import pickle
from functools import wraps

from django_redis import get_redis_connection

redis_conn = get_redis_connection("default")


def redis_cache(ttl):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached_data = redis_conn.get(cache_key)

            if cached_data:
                print("hit")
                return pickle.loads(cached_data)
            else:
                print("miss")
                result = func(*args, **kwargs)
                redis_conn.setex(cache_key, ttl, pickle.dumps(result))
                return result

        return wrapper

    return decorator
