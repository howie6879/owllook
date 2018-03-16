#!/usr/bin/env python
"""
 Created by howie.hu at 14/03/2018.
 纵横小说信息提取：http://book.zongheng.com/store/c0/c0/b9/u0/p1/v9/s9/t0/ALL.html
"""

import os
import time

from pymongo import MongoClient

from talonspider import Spider, Item, TextField, AttrField, Request
from talospider.utils import get_random_user_agent

os.environ['MODE'] = 'PRO'
from owllook.database.mongodb import MotorBaseOld
from owllook.utils.tools import async_callback


class MongoDb:
    _db = None
    MONGODB = {
        'MONGO_HOST': '127.0.0.1',
        'MONGO_PORT': '',
        'MONGO_USERNAME': '',
        'MONGO_PASSWORD': '',
        'DATABASE': 'owllook'
    }

    def client(self):
        # motor
        self.mongo_uri = 'mongodb://{account}{host}:{port}/'.format(
            account='{username}:{password}@'.format(
                username=self.MONGODB['MONGO_USERNAME'],
                password=self.MONGODB['MONGO_PASSWORD']) if self.MONGODB['MONGO_USERNAME'] else '',
            host=self.MONGODB['MONGO_HOST'] if self.MONGODB['MONGO_HOST'] else 'localhost',
            port=self.MONGODB['MONGO_PORT'] if self.MONGODB['MONGO_PORT'] else 27017)
        return MongoClient(self.mongo_uri)

    @property
    def db(self):
        if self._db is None:
            self._db = self.client()[self.MONGODB['DATABASE']]

        return self._db


class ZHNovelsItem(Item):
    target_item = TextField(css_select='ul.main_con>li')
    novel_url = AttrField(css_select='span.chap>a.fs14', attr='href')
    novel_name = TextField(css_select='span.chap>a.fs14')
    novel_author = TextField(css_select='span.author>a')
    novel_author_home_url = AttrField(css_select='span.author>a', attr='href')

    # def tal_novel_url(self, novel_url):
    # return 'http:' + novel_url

    def tal_novel_author(self, novel_author):
        if novel_author:
            if isinstance(novel_author, list):
                novel_author = novel_author[0].text
            return novel_author
        else:
            return ''

            # def tal_novel_author_home_url(self, novel_author_home_url):
            #     if isinstance(novel_author_home_url, list):
            #         novel_author_home_url = novel_author_home_url[0].get('href').strip()
            #     return 'http:' + novel_author_home_url


class ZHNovelsSpider(Spider):
    start_urls = ['http://book.zongheng.com/store/c0/c0/b9/u0/p1/v9/s9/t0/ALL.html']
    headers = {
        "User-Agent": get_random_user_agent()
    }
    set_mul = True
    request_config = {
        'RETRIES': 3,
        'DELAY': 1,
        'TIMEOUT': 10
    }
    all_novels_col = MongoDb().db.all_novels

    def parse(self, res):
        # 752
        urls = ['http://book.zongheng.com/store/c0/c0/b9/u0/p{i}/v9/s9/t0/ALL.html'.format(i=i) for i in range(1, 752)]
        for url in urls:
            headers = {
                "User-Agent": get_random_user_agent()
            }
            yield Request(url, request_config=self.request_config, headers=headers, callback=self.parse_item)

    def parse_item(self, res):
        items_data = ZHNovelsItem.get_items(html=res.html)

        for item in items_data:
            if item.novel_url:
                res_dic = {
                    'novel_url': item.novel_url,
                    'novel_name': item.novel_name,
                    'novel_author': item.novel_author,
                    'novel_author_home_url': item.novel_author_home_url,
                    'spider': 'zongheng',
                    'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
                }
                if self.all_novels_col.find_one(
                        {"novel_name": item.novel_name, 'novel_author': item.novel_author}) is None:
                    self.all_novels_col.insert_one(res_dic)
                    # async_callback(self.save, res_dic=res_dic)
                    print(item.novel_name + ' - 抓取成功')

    async def save(self, **kwargs):
        # 存进数据库
        res_dic = kwargs.get('res_dic')
        try:
            motor_db = MotorBaseOld().db
            await motor_db.all_novels.update_one({
                'novel_url': res_dic['novel_url'], 'novel_author': res_dic['novel_name']},
                {'$set': res_dic},
                upsert=True)
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    # 其他多item示例：https://gist.github.com/howie6879/3ef4168159e5047d42d86cb7fb706a2f
    ZHNovelsSpider.start()
