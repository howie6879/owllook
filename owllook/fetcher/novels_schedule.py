#!/usr/bin/env python
import asyncio
import uvloop
import schedule
import time
import sys

sys.path.append('../../')

from owllook.fetcher.cache import update_all_books


def update_all_books_schedule():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(update_all_books())
    loop.run_until_complete(task)
    return task.result()


# python novels_schedule.py
schedule.every(120).minutes.do(update_all_books_schedule)

while True:
    schedule.run_pending()
    time.sleep(1)
