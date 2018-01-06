#!/usr/bin/env python
import asyncio
import uvloop

from functools import wraps


def singleton(cls):
    """
    A singleton created by using decorator
    :param cls: cls
    :return: instance
    """
    _instances = {}

    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]

    return instance


def async_callback(func, **kwargs):
    """
    Call the asynchronous function
    :param func: a async function
    :param kwargs: params
    :return: result
    """
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(func(**kwargs))
    loop.run_until_complete(task)
    return task.result()
