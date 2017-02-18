#!/usr/bin/env python
import uvloop
import asyncio
import time
from pprint import pprint
from novel_search.fetcher.novel import search

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def novel_task(name, is_web=1):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(search(name, is_web))
    loop.run_until_complete(task)
    return task.result()


start = time.time()
result = novel_task('择天记 阅读 小说', 1)
pprint(result)
print(time.time() - start)
