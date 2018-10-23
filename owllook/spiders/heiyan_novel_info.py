#!/usr/bin/env python
"""
 Created by howie.hu at 30/03/2018.
"""
import time

from pprint import pprint

from ruia import Spider, Item, TextField, AttrField
from ruia_ua import middleware as ua_middleware

from owllook.database.mongodb import MotorBase


class HYNovelInfoItem(Item):
    """
    定义继承自item的Item类
    """
    novel_name = AttrField(css_select="meta[property='og:title']", attr='content')
    author = AttrField(css_select="meta[property='og:novel:author']", attr='content')
    cover = AttrField(css_select="meta[property='og:image']", attr='content')
    abstract = AttrField(css_select="meta[property='og:description']", attr='content')
    status = AttrField(css_select="meta[property='og:novel:status']", attr='content')
    novels_type = AttrField(css_select="meta[property='og:novel:category']", attr='content')
    novel_chapter_url = AttrField(css_select='div#voteList a.index', attr='href')
    latest_chapter = AttrField(css_select="meta[property='og:novel:latest_chapter_name']", attr='content')
    latest_chapter_url = AttrField(css_select="meta[property='og:novel:latest_chapter_url']", attr='content')
    latest_chapter_time = AttrField(css_select="meta[property='og:novel:update_time']", attr='content')

    # novel_name = TextField(css_select='div.c-left>div.mod>div.hd>h2')
    # author = TextField(css_select='div.author-zone div.right a.name strong')
    # cover = AttrField(css_select='img.book-cover', attr='src')
    # abstract = TextField(css_select='pre.note')
    # status = ''
    # novels_type = TextField(css_select='div.c-left>div.mod>div.hd>p.infos>span.cate>a')
    # latest_chapter = ''
    # novel_chapter_url = AttrField(css_select='div#voteList a.index', attr='href')

    async def clean_cover(self, cover):
        if 'https' in cover:
            return cover
        else:
            return cover.replace('http', 'https')

    async def clean_novels_type(self, novels_type):
        types_dict = {
            '社会': '都市'
        }
        print(types_dict.get(str(novels_type).strip(), novels_type))
        return types_dict.get(str(novels_type).strip(), novels_type)

    async def clean_latest_chapter_time(self, latest_chapter_time):
        return latest_chapter_time.replace(u'今天', str(time.strftime("%Y-%m-%d ", time.localtime()))).replace(u'昨日', str(
            time.strftime("%Y-%m-%d ", time.localtime(time.time() - 24 * 60 * 60))))


class HYNovelInfoSpider(Spider):
    start_urls = []
    request_config = {
        'RETRIES': 3,
        'TIMEOUT': 10
    }

    async def parse(self, res):
        self.motor_db = MotorBase(loop=self.loop).get_db()
        item = await HYNovelInfoItem.get_item(html=res.html)

        item_data = {
            'novel_name': item.novel_name,
            'author': item.author,
            'cover': item.cover,
            'abstract': item.abstract,
            'status': item.status,
            'novels_type': item.novels_type,
            'novel_chapter_url': item.novel_chapter_url,
            'latest_chapter': item.latest_chapter,
            'latest_chapter_time': item.latest_chapter_time,
            'spider': 'heiyan',
            'target_url': res.url,
            'updated_at': time.strftime("%Y-%m-%d %X", time.localtime())
        }

        print('获取 {} 小说信息成功'.format(item_data['novel_name']))
        await self.save(res_dic=item_data)

    async def save(self, res_dic):
        # 存进数据库
        try:
            motor_db = MotorBase().get_db()
            await motor_db.all_novels_info.update_one({
                'novel_name': res_dic['novel_name'], 'spider': 'heiyan'},
                {'$set': res_dic},
                upsert=True)
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    HYNovelInfoSpider.start_urls = ['http://www.heiyan.com/book/62599']
    # HYNovelInfoSpider.start_urls = [each.get('novel_url', '') for each in search_author('火星引力', 'qidian')]
    print(HYNovelInfoSpider.start_urls)
    HYNovelInfoSpider.start(middleware=ua_middleware)
