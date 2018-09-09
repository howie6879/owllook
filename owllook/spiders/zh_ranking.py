#!/usr/bin/env python
"""
 Created by howie.hu at 29/11/2017.
"""
import asyncio
import time

from aspider import Spider, Request
from aspider.utils import get_random_user_agent

from owllook.database.mongodb import MotorBaseOld
from owllook.utils.tools import async_callback


class BdNovelSpider(Spider):
    start_urls = ['http://book.zongheng.com/api/rank/getZongHengRankList.htm?rankType=1&pageNum=1&pageSize=20']

    headers = {
        "User-Agent": asyncio.get_event_loop().run_until_complete(get_random_user_agent())
    }
    concurrency = 3
    res_type = 'json'

    async def parse(self, res):
        data = res.body
        result = []
        res_dic = {}
        if data:
            for each_data in data:
                data = {
                    'name': each_data.get('bookName', ''),
                    'type': each_data.get('bookShortCateName', ''),
                    'num': each_data.get('orderNo', ''),
                    'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
                }
                result.append(data)
            res_dic['data'] = result
            res_dic['target_url'] = res.url
            res_dic['type'] = "全部类别"
            res_dic['spider'] = "zh_bd_novels"
        await self.save(res_dic)

    async def save(self, res_dic):
        try:
            motor_db = MotorBaseOld().db
            await motor_db.novels_ranking.update_one({
                'target_url': res_dic['target_url']},
                {'$set': {
                    'data': res_dic['data'],
                    'spider': res_dic['spider'],
                    'type': res_dic['type'],
                    'finished_at': time.strftime("%Y-%m-%d %X", time.localtime())
                }},
                upsert=True)
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    BdNovelSpider.start()
