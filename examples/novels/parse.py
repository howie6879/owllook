#!/usr/bin/env python
import aiohttp
import asyncio
import time
import uvloop

from pprint import pprint

from owllook.fetcher.function import target_fetch

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def novel_task(url):
    loop = asyncio.get_event_loop()

    task = asyncio.ensure_future(target_fetch(url, {}))
    loop.run_until_complete(task)
    return task.result()


start = time.time()
# result = novel_task('http://www.shuge.net/html/98/98044')
result = novel_task('http://www.biqugexsw.com/1_1020/')
pprint(result)
print(time.time() - start)
