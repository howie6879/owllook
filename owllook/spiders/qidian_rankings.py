#!/usr/bin/env python
from talonspider import Spider, Item, TextField, AttrField
from talonspider.utils import get_random_user_agent
import time


class RankingItem(Item):
    target_item = TextField(css_select='.rank-list')
    ranking_title = TextField(css_select='h3.wrap-title')
    more = AttrField(css_select='h3>a.more', attr='href')
    book_list = TextField(css_select='div.book-list>ul>li')

    def tal_more(self, more):
        return "http:" + more


class NameItem(Item):
    top_name = TextField(css_select='h4>a')
    other_name = TextField(css_select='a.name')


class QidianRankingSpider(Spider):
    start_urls = ["http://r.qidian.com/?chn=" + str(url) for url in [-1, 21, 1, 2, 22, 4, 15, 6, 5, 7, 8, 9, 10, 12]]
    headers = {
        "User-Agent": get_random_user_agent()
    }
    set_mul = True

    def parse(self, html):
        items_data = RankingItem.get_items(html=html)
        result = []
        for item in items_data:
            each_book_list = []
            # 只取排名前十的书籍数据
            for index, value in enumerate(item.book_list[:10]):
                item_data = NameItem.get_item(html_etree=value)
                name = item_data.get('top_name') or item_data.get('other_name')
                each_book_list.append({
                    'num': index + 1,
                    'name': name
                })
            data = {
                'title': item.ranking_title,
                'more': item.more,
                'book_list': each_book_list,
                'updated_at': time.strftime("%Y-%m-%d %X", time.localtime()),
                'spider': 'qidian'
            }
            result.append(data)
        print(result)


if __name__ == '__main__':
    QidianRankingSpider().start()
