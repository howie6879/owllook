#!/usr/bin/env python
"""
 Created by howie.hu at 14/03/2018.
 纵横小说信息提取：http://book.zongheng.com/store/c0/c0/b9/u0/p1/v9/s9/t0/ALL.html
"""
import asyncio
import os
import time

from ruia import Spider, Item, TextField, AttrField, Request
from ruia_ua import middleware as ua_middleware

# os.environ['MODE'] = 'PRO'
from owllook.database.mongodb import MotorBase
from owllook.spiders.middlewares import owl_middleware

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)


class ZHNovelsItem(Item):
    target_item = TextField(css_select='div.store_collist div.bookbox')
    novel_url = AttrField(css_select='div.bookinfo div.bookname a', attr='href')
    novel_name = TextField(css_select='div.bookinfo div.bookname a')
    novel_author = TextField(css_select='div.bookilnk a:nth-child(1)')
    novel_author_home_url = AttrField(css_select='div.bookilnk a:nth-child(1)', attr='href')
    novel_type = TextField(css_select='div.bookilnk a:nth-child(2)')
    novel_cover = AttrField(css_select='div.bookimg img', attr='src')
    novel_abstract = TextField(css_select='div.bookintro')
    novel_latest_chapter = TextField(css_select='div.bookupdate a')

    # def tal_novel_url(self, novel_url):
    # return 'http:' + novel_url

    async def clean_novel_author(self, novel_author):
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

    request_config = {
        'RETRIES': 8,
        'DELAY': 0,
        'TIMEOUT': 3
    }
    concurrency = 60
    motor_db = MotorBase(loop=loop).get_db()

    async def parse(self, res):
        items_data = await ZHNovelsItem.get_items(html=res.html)
        tasks = []
        for item in items_data:
            if item.novel_url:
                res_dic = {
                    'novel_url': item.novel_url,
                    'novel_name': item.novel_name,
                    'novel_author': item.novel_author,
                    'novel_author_home_url': item.novel_author_home_url,
                    'novel_type': item.novel_type,
                    'novel_cover': item.novel_cover,
                    'novel_abstract': item.novel_abstract,
                    'novel_latest_chapter': item.novel_latest_chapter,
                    'spider': 'zongheng',
                    'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
                }
                tasks.append(asyncio.ensure_future(self.save(res_dic)))
                # if self.all_novels_col.find_one(
                #         {"novel_name": item.novel_name, 'novel_author': item.novel_author}) is None:
                #     self.all_novels_col.insert_one(res_dic)
                #     # async_callback(self.save, res_dic=res_dic)
                #     print(item.novel_name + ' - 抓取成功')
        good_nums = 0
        if tasks:
            done_list, pending_list = await asyncio.wait(tasks)
            for task in done_list:
                if task.result():
                    good_nums += 1
        print(f"共{len(tasks)}本小说，抓取成功{good_nums}本")

    async def save(self, res_dic):
        # 存进数据库
        res_dic = res_dic
        try:

            await self.motor_db.all_novels.update_one({
                'novel_url': res_dic['novel_url'], 'novel_name': res_dic['novel_name']},
                {'$set': res_dic},
                upsert=True)
            print(res_dic['novel_name'] + ' - 抓取成功')
            return True
        except Exception as e:
            self.logger.exception(e)
            return False


if __name__ == '__main__':
    # 其他多item示例：https://gist.github.com/howie6879/3ef4168159e5047d42d86cb7fb706a2f
    # 51793
    for page in range(0, 10):
        print(f"正在爬取第{page}页")
        start_page = page * 100
        end_page = start_page + 100
        if end_page > 999:
            end_page = 999
        ZHNovelsSpider.start_urls = ['http://book.zongheng.com/store/c0/c0/b9/u0/p{i}/v9/s9/t0/ALL.html'.format(i=i) for
                                     i in
                                     range(start_page, end_page)]
        # 其他多item示例：https://gist.github.com/howie6879/3ef4168159e5047d42d86cb7fb706a2f
        ZHNovelsSpider.start(loop=loop, middleware=[ua_middleware, owl_middleware], close_event_loop=False)
