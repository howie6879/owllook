#!/usr/bin/env python
"""
 Created by howie.hu at 2018/8/13.
"""

import os
import schedule
import sys
import time

# os.environ['MODE'] = 'PRO'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from owllook.config import CONFIG
from owllook.spiders import QidianRankingSpider, BdNovelSpider


def start_spider():
    QidianRankingSpider.start()
    BdNovelSpider.start()


def refresh_task(spider_interval):
    schedule.every(spider_interval).minutes.do(start_spider)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    spider_interval = CONFIG.SCHEDULED_DICT['SPIDER_INTERVAL']
    refresh_task(spider_interval=spider_interval)
