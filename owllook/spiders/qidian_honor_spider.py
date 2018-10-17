#!/usr/bin/env python
"""
 Created by howie.hu at 11/03/2018.
 获取起点荣誉数据，如：https://book.qidian.com/honor/1009704712
 荣誉类型：
  - 推荐票
  - 收藏
  - 点击
"""

from ruia import Spider, Item, TextField
from ruia_ua import middleware


class QidianHonorItem(Item):
    target_item = TextField(css_select='li.cf')
    honor_text = TextField(css_select='span.decs')
    honor_time = TextField(css_select='span.time')


class QidianHonorSpider(Spider):
    start_urls = ['https://book.qidian.com/honor/1009531496']

    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 10
    }

    async def parse(self, res):
        items_data = await QidianHonorItem.get_items(html=res.html)
        click_list, col_list, rec_list, other_list = [], [], [], []
        for item in items_data:
            data = {
                'honor_text': item.honor_text,
                'honor_time': item.honor_time,
            }
            if "点击" in data['honor_text'] and '月点击' not in data['honor_text']:
                click_list.append(data)
            elif "收藏" in data['honor_text']:
                col_list.append(data)
            elif "推荐票" in data['honor_text']:
                rec_list.append(data)
            else:
                other_list.append(data)
        print('点击荣誉\n')
        for i in click_list:
            print(str(i.get('honor_time')) + " - " + str(i.get('honor_text')))

        print('收藏荣誉\n')
        for i in col_list:
            print(str(i.get('honor_time')) + " - " + str(i.get('honor_text')))

        print('推荐票荣誉\n')
        for i in rec_list:
            print(str(i.get('honor_time')) + " - " + str(i.get('honor_text')))

        print('强推荣誉\n')
        for i in other_list:
            print(str(i.get('honor_time')) + " - " + str(i.get('honor_text')))


if __name__ == '__main__':
    QidianHonorSpider.start(middleware=middleware)
