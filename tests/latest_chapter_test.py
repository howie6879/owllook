#!/usr/bin/env python
import asyncio
import os
import time
import uvloop

from pprint import pprint

os.environ['MODE'] = 'PRO'
from owllook.fetcher.cache import get_the_latest_chapter, update_all_books

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def latest_chapter_task(url):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(get_the_latest_chapter(url))
    loop.run_until_complete(task)
    return task.result()


def update_all():
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(update_all_books())
    loop.run_until_complete(task)
    return task.result()


start = time.time()
chapter_url = "/chapter?url=http://www.8535.org/xuanhuan/139075/&novels_name=圣墟"

result = latest_chapter_task(chapter_url)
pprint(result)
print(time.time() - start)
