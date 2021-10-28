from functools import wraps
from time import time

from slapp_py.helpers.str_helper import truncate


def debug_time(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%s, %s] took: %2.4f sec' % (f.__name__, truncate(str(repr(args)), 100, '…'), truncate(str(repr(kw)), 100, '…'), te-ts))
        return result
    return wrap


def debug_time_async(f):
    async def wrapper(*args, **kw):
        ts = time()
        result = await f(*args, **kw)
        te = time()
        print('func:%r args:[%s, %s] took: %2.4f sec' %
              (f.__name__, truncate(str(repr(args)), 100, '…'), truncate(str(repr(kw)), 100, '…'), te - ts))
        return result
    return wrapper
