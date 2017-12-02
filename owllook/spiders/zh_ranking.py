#!/usr/bin/env python
"""
 Created by howie.hu at 29/11/2017.
"""
import os
import time

from talonspider import Spider, Request
from talonspider.utils import get_random_user_agent
from pprint import pprint

os.environ['MODE'] = 'PRO'
from owllook.database.mongodb import MotorBaseOld
from owllook.utils.tools import async_callback


class BdNovelSpider(Spider):
    start_urls = ['http://book.zongheng.com/api/rank/getZongHengRankList.htm?rankType=1&pageNum=1&pageSize=20']
    set_mul = True
    headers = {
        "User-Agent": get_random_user_agent()
    }

    def start_request(self):
        for url in self.start_urls:
            yield Request(url=url,
                          request_config=getattr(self, 'request_config'),
                          headers=getattr(self, 'headers', None),
                          callback=self.parse, file_type="json")

    def parse(self, res):
        data = res.html
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
        async_callback(self.save, res_dic=res_dic)

    async def save(self, **kwargs):
        # 存进数据库
        res_dic = kwargs.get('res_dic')
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
