#!/usr/bin/env python
import asyncio
import time

from ruia import Spider, Item, AttrField, HtmlField, TextField
from ruia_ua import middleware

from owllook.database.mongodb import MotorBaseOld


class RankingItem(Item):
    target_item = TextField(css_select='.rank-list')
    ranking_title = TextField(css_select='h3.wrap-title')
    more = AttrField(css_select='h3>a.more', attr='href')
    book_list = HtmlField(css_select='div.book-list>ul>li', many=True)

    async def clean_ranking_title(self, ranking_title):
        if isinstance(ranking_title, list):
            return ranking_title[0].text
        else:
            return str(ranking_title).split('榜')[0] + '榜'

    async def clean_more(self, more):
        return "https:" + more


class NameItem(Item):
    top_name = TextField(css_select='h4', default='')
    other_name = TextField(css_select='a.name', default='')


class QidianRankingSpider(Spider):
    start_urls = [f"https://www.qidian.com/rank/?chn={key}" for key in
                  [-1, 21, 1, 2, 22, 4, 15, 6, 5, 7, 8, 9, 10, 12]]

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
        result = []
        res_dic = {}
        async for item in RankingItem.get_items(html=res.html):
            each_book_list = []
            # 只取排名前十的书籍数据
            for index, value in enumerate(item.book_list[:10]):
                item_data = await NameItem.get_item(html=value)
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
    QidianRankingSpider.start(middleware=middleware)
