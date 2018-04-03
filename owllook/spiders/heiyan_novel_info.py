#!/usr/bin/env python
"""
 Created by howie.hu at 30/03/2018.
"""
import time

from pprint import pprint

from talospider import Spider, Item, TextField, AttrField
from talospider.utils import get_random_user_agent

from owllook.database.mongodb import PyMongoDb, MotorBase
from owllook.utils.tools import async_callback


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

    def tal_cover(self, cover):
        if 'https' in cover:
            return cover
        else:
            return cover.replace('http', 'https')

    def tal_novels_type(self, novels_type):
        types_dict = {
            '社会': '都市'
        }
        print(types_dict.get(str(novels_type).strip(), novels_type))
        return types_dict.get(str(novels_type).strip(), novels_type)

    def tal_latest_chapter_time(self, latest_chapter_time):
        return latest_chapter_time.replace(u'今天', str(time.strftime("%Y-%m-%d ", time.localtime()))).replace(u'昨日', str(
            time.strftime("%Y-%m-%d ", time.localtime(time.time() - 24 * 60 * 60))))


class HYNovelInfoSpider(Spider):
    start_urls = []
    request_config = {
        'RETRIES': 3,
        'TIMEOUT': 10
    }

    headers = {
        "User-Agent": get_random_user_agent()
    }

    all_novels_col = PyMongoDb().db.all_novels
    all_novels_info_col = PyMongoDb().db.all_novels_info

    def parse(self, res):
        item_data = HYNovelInfoItem.get_item(html=res.html)
        item_data['target_url'] = res.url
        item_data['spider'] = 'heiyan'
        item_data['updated_at'] = time.strftime("%Y-%m-%d %X", time.localtime())
        print('获取 {} 小说信息成功'.format(item_data['novel_name']))
        print(item_data)
        self.all_novels_info_col.update({'novel_name': item_data['novel_name'], 'spider': 'heiyan'}, item_data,
                                        upsert=True)
        async_callback(self.save, res_dic=item_data)

    async def save(self, **kwargs):
        # 存进数据库
        res_dic = kwargs.get('res_dic')
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
    HYNovelInfoSpider.start()
