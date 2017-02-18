#!/usr/bin/env python
# !/usr/bin/env python
import uvloop
import asyncio
import time
from pprint import pprint
from novels_search.fetcher.parse import novel_search

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def novel_task(url):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(novel_search(url))
    loop.run_until_complete(task)
    return task.result()


start = time.time()
result = novel_task('http://www.biquge.com/0_174/')
pprint(result)
print(time.time() - start)
