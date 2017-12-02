# !/usr/bin/env python
import schedule
import time
import sys
import os

os.environ['MODE'] = 'PRO'
sys.path.append('../../')

from owllook.spiders import QidianRankingSpider, BdNovelSpider


def start_spider():
    QidianRankingSpider().start()
    BdNovelSpider().start()


# python novels_schedule.py
schedule.every(60).minutes.do(start_spider)

while True:
    schedule.run_pending()
    time.sleep(1)
