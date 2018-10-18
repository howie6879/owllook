#!/usr/bin/env python
"""
 Created by howie.hu at 25/02/2018.
 Target URI: https://www.qidian.com/all
        Param:?page=1
"""
import asyncio
import os
import time

from ruia import Spider, Item, TextField, AttrField
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


class QidianNovelsItem(Item):
    target_item = TextField(css_select='ul.all-img-list>li')
    novel_url = AttrField(css_select='div.book-img-box>a', attr='href')
    novel_name = TextField(css_select='div.book-mid-info>h4')
    novel_author = TextField(css_select='div.book-mid-info>p.author>a.name')
    novel_author_home_url = AttrField(css_select='div.book-mid-info>p.author>a.name', attr='href')
    novel_type = TextField(css_select='div.book-mid-info > p.author > a:nth-child(4)')
    novel_cover = AttrField(css_select='div.book-img-box img', attr='src')
    novel_abstract = TextField(css_select='div.book-mid-info p.intro')

    # novel_latest_chapter = TextField(css_select='div.bookupdate a')

    async def clean_novel_url(self, novel_url):
        return 'https:' + novel_url

    async def clean_novel_author(self, novel_author):
        if isinstance(novel_author, list):
            novel_author = novel_author[0].text
        return novel_author

    async def clean_novel_author_home_url(self, novel_author_home_url):
        if isinstance(novel_author_home_url, list):
            novel_author_home_url = novel_author_home_url[0].get('href').strip()
        return 'https:' + novel_author_home_url

    async def clean_novel_cover(self, novel_cover):
        return 'https:' + novel_cover


class QidianNovelsSpider(Spider):
    # start_urls = ['https://www.qidian.com/all?page=1']

    request_config = {
        'RETRIES': 10,
        'DELAY': 0,
        'TIMEOUT': 3
    }
    concurrency = 100
    motor_db = MotorBase(loop=loop).get_db()

    async def parse(self, res):
        items_data = await QidianNovelsItem.get_items(html=res.html)
        tasks = []
        for item in items_data:
            res_dic = {
                'novel_url': item.novel_url,
                'novel_name': item.novel_name,
                'novel_author': item.novel_author,
                'novel_author_home_url': item.novel_author_home_url,
                'novel_type': item.novel_type,
                'novel_cover': item.novel_cover,
                'novel_abstract': item.novel_abstract,
                'spider': 'qidian',
                'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
            }
            tasks.append(asyncio.ensure_future(self.save(res_dic)))

        good_nums = 0
        if tasks:
            done_list, pending_list = await asyncio.wait(tasks)
            for task in done_list:
                if task.result():
                    good_nums += 1
        print(f"共{len(tasks)}本小说，抓取成功{good_nums}本")

    async def save(self, res_dic):
        # 存进数据库
        try:
            await self.motor_db.all_novels.update_one(
                {'novel_url': res_dic['novel_url'], 'novel_name': res_dic['novel_name']},
                {'$set': res_dic},
                upsert=True)
            print(res_dic['novel_name'] + ' - 抓取成功')
            return True
        except Exception as e:
            self.logger.exception(e)
            return False


if __name__ == '__main__':
    # 51793
    for page in range(133, 519):
        print(f"正在爬取第{page}页")
        start_page = page * 100
        end_page = start_page + 100
        if end_page > 51793:
            end_page = 51793
        QidianNovelsSpider.start_urls = ['https://www.qidian.com/all?page={i}'.format(i=i) for i in
                                         range(start_page, end_page)]
        # 其他多item示例：https://gist.github.com/howie6879/3ef4168159e5047d42d86cb7fb706a2f
        QidianNovelsSpider.start(loop=loop, middleware=[ua_middleware, owl_middleware], close_event_loop=False)
