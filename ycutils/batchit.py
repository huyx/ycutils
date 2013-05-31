# -*- coding: utf-8 -*-
"""批量处理

允许用户提供一个批处理函数，批量处理操作

* 支持批量操作
* 用户可以随时调用 func.batch 批量执行操作

用法：

    def batch_op(batch_args):
        for args, kwargs in batch_args:
            print args, kwargs

    @batchit(batch_op, 10, 10)
    def op(*args, **kwargs):
        print args, kwargs

"""
from functools import wraps
import time

def batchit(batch_func, count, expiry=None):
    expiry = expiry or 3600

    def decorator(func):
        func.queue = []
        func.timestamp = time.time() + expiry

        def batch():
            batch_func(func.queue)
            del func.queue[:]
            func.timestamp = time.time() + expiry

        func.batch = batch

        @wraps(func)
        def wrapper(*args, **kwargs):
            func.queue.append((args, kwargs))
            if len(func.queue) == count:
                func.batch()
            elif func.timestamp < time.time():
                func.batch()

        return wrapper

    return decorator

if __name__ == '__main__':
    def batch_f(batch_args):
        for args, kwargs in batch_args:
            print args, kwargs,
        print
    
    @batchit(batch_f, 5, 0.5)
    def f(*args, **kwargs):
        print args, kwargs

    for i in xrange(20):
        time.sleep(0.2)
        f(i, i=i)

    f.batch()
