# -*- coding:utf-8 -*-
# !/usr/bin/env python
import time

from pprint import pprint

from pymongo import MongoClient
from talospider import Spider, Item, TextField, AttrField


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


class QidianNovelInfoItem(Item):
    """
    定义继承自item的Item类
    """
    novel_name = TextField(css_select='.book-info>h1>em')
    author = TextField(css_select='a.writer')
    # 当提取的值是属性的时候，要定义AttrField
    cover = AttrField(css_select='a#bookImg>img', attr='src')
    abstract = TextField(css_select='div.book-intro>p')
    status = TextField(css_select='p.tag>span.blue')
    novels_type = TextField(css_select='p.tag>a.red')
    latest_chapter = TextField(css_select='li.update>div.detail>p.cf>a')
    latest_chapter_time = TextField(css_select='div.detail>p.cf>em')

    def tal_cover(self, cover):
        return 'http:' + cover

    def tal_status(self, status):
        """
        当目标值的对象只有一个，默认将值提取出来，否则返回list，可以在这里定义一个函数进行循环提取
        :param ele_tag:
        :return:
        """
        return '#'.join([i.text for i in status])

    def tal_novels_type(self, novels_type):
        return '#'.join([i.text for i in novels_type])

    def tal_latest_chapter_time(self, latest_chapter_time):
        return latest_chapter_time.replace(u'今天', str(time.strftime("%Y-%m-%d ", time.localtime()))).replace(u'昨日', str(
            time.strftime("%Y-%m-%d ", time.localtime(time.time() - 24 * 60 * 60))))


class QidianNovelInfoSpider(Spider):
    start_urls = []
    request_config = {
        'RETRIES': 3,
        'TIMEOUT': 10
    }
    pool_size = 4
    set_mul = True

    all_novels_col = MongoDb().db.all_novels
    all_novels_info_col = MongoDb().db.all_novels_info

    def parse(self, res):
        item_data = QidianNovelInfoItem.get_item(html=res.html)
        # 这里可以保存获取的item
        # for python 2.7
        # import json
        # item_data = json.dumps(item_data, ensure_ascii=False)
        item_data['target_url'] = res.url
        item_data['spider'] = 'qidian'
        item_data['updated_at'] = time.strftime("%Y-%m-%d %X", time.localtime())
        print('获取 {} 小说信息成功'.format(item_data['novel_name']))
        self.all_novels_info_col.update({'novel_name': item_data['novel_name']}, item_data, upsert=True)


if __name__ == '__main__':
    import random

    # 其他多item示例：https://gist.github.com/howie6879/3ef4168159e5047d42d86cb7fb706a2f
    QidianNovelInfoSpider.start_urls = ['http://book.qidian.com/info/1004608738', 'http://book.qidian.com/info/3602691',
                               'http://book.qidian.com/info/3347595', 'http://book.qidian.com/info/1887208']


    # QidianSpider.start()

    def all_novels_info():
        all_urls = []

        for each in QidianNovelInfoSpider.all_novels_col.find():
            all_urls.append(each['novel_url'])
        random.shuffle(all_urls)

        QidianNovelInfoSpider.start_urls = all_urls
        QidianNovelInfoSpider.start()


    all_novels_info()
