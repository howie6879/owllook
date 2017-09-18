#!/usr/bin/env python

# !/usr/bin/env python
import schedule
import time
import sys
import os

os.environ['MODE'] = 'PRO'
sys.path.append('../../')

from owllook.spiders import QidianRankingSpider

# python novels_schedule.py
schedule.every(60).minutes.do(QidianRankingSpider().start)

while True:
    schedule.run_pending()
    time.sleep(1)
