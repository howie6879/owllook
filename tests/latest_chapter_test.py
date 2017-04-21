#!/usr/bin/env python
import uvloop
import asyncio
import time
from pprint import pprint
from novels_search.fetcher.cache import get_the_latest_chapter, update_all_books

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
# chapter_url = "/chapter?url=http://www.biquge.cc/html/156/156129/&novels_name=圣墟"
chapter_url = "/chapter?url=http://www.8535.org/xuanhuan/139075/&novels_name=圣墟"
# chapter_url = "/chapter?url=http://www.50331.net/&novels_name=圣墟"
# chapter_url = "/chapter?url=http://www.biquge.tw/86_86745/&novels_name=圣墟"
# result = novel_task('http://www.shuge.net/html/98/98044')
# result = update_all()

result = latest_chapter_task(chapter_url)
pprint(result)
print(time.time() - start)
