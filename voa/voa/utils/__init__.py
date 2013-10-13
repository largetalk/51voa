import redis
import threading
from voa.settings import REDIS_SERVER

_lock = threading.Lock()
_redis = None

def get_redis():
    if _redis:
        return _redis
    global _redis
    try:
        _lock.acquire()
        _redis = redis.Redis(REDIS_SERVER)
        return _redis
    finally:
        _lock.release()

_f = lambda x:x[0] if isinstance(x, list) and len(x) else ''
