#!/usr/bin/env python
import uvloop
import asyncio
import time
from pprint import pprint
from novels_search.fetcher.so_novels import so_search as search

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def novel_task(name):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(search(name))
    loop.run_until_complete(task)
    return task.result()


start = time.time()
result = novel_task('琅琊榜 小说 免费阅读')
pprint(result)
print(time.time() - start)
