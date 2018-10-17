# -*- coding:utf-8 -*-
# !/usr/bin/env python
import os
import time

from ruia import Spider, Item, TextField, AttrField
from ruia_ua import middleware

os.environ['MODE'] = 'PRO'

from owllook.database.mongodb import MotorBaseOld


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

    async def clean_cover(self, cover):
        return 'http:' + cover

    async def clean_status(self, status):
        """
        当目标值的对象只有一个，默认将值提取出来，否则返回list，可以在这里定义一个函数进行循环提取
        :param ele_tag:
        :return:
        """
        return '#'.join([i.text for i in status])

    async def clean_novels_type(self, novels_type):
        return '#'.join([i.text for i in novels_type])

    async def clean_latest_chapter_time(self, latest_chapter_time):
        return latest_chapter_time.replace(u'今天', str(time.strftime("%Y-%m-%d ", time.localtime()))).replace(u'昨日', str(
            time.strftime("%Y-%m-%d ", time.localtime(time.time() - 24 * 60 * 60))))


class QidianNovelInfoSpider(Spider):
    request_config = {
        'RETRIES': 3,
        'TIMEOUT': 10
    }

    async def parse(self, res):
        motor_db = MotorBaseOld().db
        item = await QidianNovelInfoItem.get_item(html=res.html)
        item_data = {
            'novel_name': item.novel_name,
            'author': item.author,
            'cover': item.cover,
            'abstract': item.abstract,
            'status': item.status,
            'novels_type': item.novels_type,
            'latest_chapter': item.latest_chapter,
            'latest_chapter_time': item.latest_chapter_time,
            'spider': 'qidian',
            'target_url': res.url,
            'updated_at': time.strftime("%Y-%m-%d %X", time.localtime())
        }
        print('获取 {} 小说信息成功'.format(item.novel_name))
        await motor_db.all_novels_info.update_one(
            {'novel_name': item_data['novel_name'], 'spider': item_data['spider']},
            {'$set': item_data},
            upsert=True)


if __name__ == '__main__':
    import random

    # 其他多item示例：https://gist.github.com/howie6879/3ef4168159e5047d42d86cb7fb706a2f
    QidianNovelInfoSpider.start_urls = ['https://book.qidian.com/info/1004608738',
                                        'https://book.qidian.com/info/3602691',
                                        'https://book.qidian.com/info/3347595', 'https://book.qidian.com/info/1887208']

    # QidianNovelInfoSpider.start_urls = all_urls
    QidianNovelInfoSpider.start(middleware=middleware)
