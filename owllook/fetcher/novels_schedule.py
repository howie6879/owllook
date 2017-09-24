#!/usr/bin/env python
import asyncio
import uvloop
import schedule
import time
import sys
import os

os.environ['MODE'] = 'PRO'
sys.path.append('../../')

from owllook.fetcher.cache import update_all_books

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


def update_all_books_schedule():
    task = asyncio.ensure_future(update_all_books(loop))
    loop.run_until_complete(task)
    return task.result() or None


# python novels_schedule.py
schedule.every(90).minutes.do(update_all_books_schedule)

while True:
    schedule.run_pending()
    time.sleep(1)
