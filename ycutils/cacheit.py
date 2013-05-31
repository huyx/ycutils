# -*- coding: utf-8 -*-
""" cacheit

特点：

 * 支持指定超时时间
 * 针对不指定超时时间的情况做了优化

用法:

    @cacheit()
    def f1():
        // ...

    @cacheit(3)
    def f2():
        // ...
"""
from functools import wraps
import time

def cacheit(expiry=None):
    def wrapper(func):
        cache = {}

        if not expiry:
            @wraps(func)
            def wrapped(*args):
                if args not in cache:
                    return cache.setdefault(args, func(*args))
                return cache[args]
        else:
            @wraps(func)
            def wrapped(*args):
                now = time.time()
                item = cache.get(args)
                if item:
                    if item[1] > now:
                        return item[0]
                value = func(*args)
                cache[args] = (value, now+expiry)
                return value

        return wrapped
    return wrapper

if __name__ == '__main__':
    @cacheit()
    def f():
        print '!f',
        return 'f'

    @cacheit(0.6)
    def g():
        print '!g',
        return 'g'

    for i in xrange(10):
        time.sleep(0.1)
        print f()
        print g()
