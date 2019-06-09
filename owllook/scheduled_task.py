#!/usr/bin/env python
"""
 Created by howie.hu at 2018/8/13.
"""

import os
import asyncio
import sys
import time

import schedule
import uvloop

os.environ['MODE'] = 'PRO'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from owllook.config import CONFIG
from owllook.spiders import QidianRankingSpider, ZHRankingSpider
from owllook.fetcher.cache import update_all_books

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


def start_spider():
    QidianRankingSpider.start()
    ZHRankingSpider.start()


def update_all_books_schedule():
    task = asyncio.ensure_future(update_all_books(loop))
    loop.run_until_complete(task)
    return task.result() or None


def refresh_task():
    schedule.every(CONFIG.SCHEDULED_DICT['SPIDER_INTERVAL']).minutes.do(start_spider)
    # schedule.every(CONFIG.SCHEDULED_DICT['NOVELS_INTERVAL']).minutes.do(update_all_books_schedule)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    start_spider()
    refresh_task()
