#!/usr/bin/env python
import uvloop
import asyncio


def async_callback(func, **kwargs):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(func(**kwargs))
    loop.run_until_complete(task)
    return task.result()
