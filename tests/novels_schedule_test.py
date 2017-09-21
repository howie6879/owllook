#!/usr/bin/env python
import asyncio
import uvloop
import os

os.environ['MODE'] = 'DEV'
from owllook.fetcher.cache import update_all_books


def update_all():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(update_all_books(loop=loop))
    loop.run_until_complete(task)
    return task.result() or None


print(update_all())
