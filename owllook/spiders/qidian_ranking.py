#!/usr/bin/env python
import asyncio
import time

from aspider import Spider, Item, TextField, AttrField
from aspider.utils import get_random_user_agent

from owllook.database.mongodb import MotorBaseOld
from owllook.utils.tools import async_callback


class RankingItem(Item):
    target_item = TextField(css_select='.rank-list')
    ranking_title = AttrField(css_select='h3.wrap-title', attr='html')
    more = AttrField(css_select='h3>a.more', attr='href')
    book_list = TextField(css_select='div.book-list>ul>li')

    async def clean_ranking_title(self, ranking_title):
        if isinstance(ranking_title, list):
            return ranking_title[0].text

    async def clean_more(self, more):
        return "http:" + more


class NameItem(Item):
    top_name = TextField(css_select='h4>a')
    other_name = TextField(css_select='a.name')


class QidianRankingSpider(Spider):
    start_urls = ["http://r.qidian.com/?chn=" + str(url) for url in [-1, 21, 1, 2, 22, 4, 15, 6, 5, 7, 8, 9, 10, 12]]

    headers = {
        "User-Agent": asyncio.get_event_loop().run_until_complete(get_random_user_agent())
    }
    concurrency = 3
    qidian_type = {
        '-1': '全部类别',
        '21': '玄幻',
        '1': '奇幻',
        '2': '武侠',
        '22': '仙侠',
        '4': '都市',
        '15': '职场',
        '6': '军事',
        '5': '历史',
        '7': '游戏',
        '8': '体育',
        '9': '科幻',
        '10': '灵异',
        '12': '二次元',
    }

    async def parse(self, res):
        items_data = await RankingItem.get_items(html_etree=res.e_html)
        result = []
        res_dic = {}
        for item in items_data:
            each_book_list = []
            # 只取排名前十的书籍数据
            for index, value in enumerate(item.book_list[:10]):
                item_data = await NameItem.get_item(html_etree=value)
                name = item_data.top_name or item_data.other_name
                each_book_list.append({
                    'num': index + 1,
                    'name': name
                })
            data = {
                'title': item.ranking_title,
                'more': item.more,
                'book_list': each_book_list,
                'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
            }
            result.append(data)
        res_dic['data'] = result
        res_dic['target_url'] = res.url
        res_dic['type'] = self.qidian_type.get(res.url.split('=')[-1])
        res_dic['spider'] = "qidian"
        await self.save(res_dic=res_dic)

    async def save(self, res_dic):
        # 存进数据库
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
    QidianRankingSpider.start()
