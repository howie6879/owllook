#!/usr/bin/env python
import uvloop
import asyncio
import time
from pprint import pprint
from owllook.fetcher.parse import novels_search

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def novel_task(url):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(novels_search(url))
    loop.run_until_complete(task)
    return task.result()


start = time.time()
#result = novel_task('http://www.shuge.net/html/98/98044')
result = novel_task('www.dingdianzw.com')
pprint(result)
print(time.time() - start)
