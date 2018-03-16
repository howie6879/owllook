# -*- coding:utf-8 -*-
# !/usr/bin/env python
import time

from pprint import pprint

from pymongo import MongoClient
from talonspider import Spider, Item, TextField, AttrField


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


class ZHNovelInfoItem(Item):
    """
    定义继承自item的Item类
    """
    novel_name = TextField(css_select='div.main div.status h1 a')
    author = TextField(css_select='div.main div.status div.booksub a')
    # 当提取的值是属性的时候，要定义AttrField
    cover = AttrField(css_select='div.main div.book_cover img', attr='src')
    abstract = TextField(css_select='div.main div.status div.info_con p')
    status = AttrField(css_select='div.main div.status h1 em', attr='title')
    novels_type = TextField(css_select='div.main div.status div.booksub a')
    novel_chapter_url = AttrField(css_select='div.main div.status div.book_btn span.list a', attr='href')

    def tal_author(self, author):
        if isinstance(author, list):
            return author[0].text
        else:
            return author

    def tal_status(self, status):
        """
        当目标值的对象只有一个，默认将值提取出来，否则返回list，可以在这里定义一个函数进行循环提取
        :param ele_tag:
        :return:
        """
        if isinstance(status, list):
            return '#'.join([i.get('title').strip().replace('作品', '') for i in status])
        else:
            return status

    def tal_novels_type(self, novels_type):
        if isinstance(novels_type, list):
            try:
                return novels_type[1].text
            except:
                return ''
        else:
            return ''


class ZHNovelInfoSpider(Spider):
    start_urls = []
    request_config = {
        'RETRIES': 3,
        'DELAY': 2,
        'TIMEOUT': 10
    }
    pool_size = 4
    set_mul = True

    all_novels_col = MongoDb().db.all_novels
    all_novels_info_col = MongoDb().db.all_novels_info

    def parse(self, res):
        item_data = ZHNovelInfoItem.get_item(html=res.html)

        item_data['target_url'] = res.url
        item_data['spider'] = 'zongheng'
        item_data['updated_at'] = time.strftime("%Y-%m-%d %X", time.localtime())
        print('获取 {} 小说信息成功'.format(item_data['novel_name']))
        self.all_novels_info_col.update({'novel_name': item_data['novel_name']}, item_data, upsert=True)


if __name__ == '__main__':
    import random

    # 其他多item示例：https://gist.github.com/howie6879/3ef4168159e5047d42d86cb7fb706a2f
    ZHNovelInfoSpider.start_urls = ['http://book.zongheng.com/book/547205.html',
                                    'http://huayu.baidu.com/book/633311.html']


    def all_novels_info():
        all_urls = []

        for each in ZHNovelInfoSpider.all_novels_col.find({'spider': 'zongheng'}):
            all_urls.append(each['novel_url'])
        random.shuffle(all_urls)

        ZHNovelInfoSpider.start_urls = all_urls
        ZHNovelInfoSpider.start()


    all_novels_info()
