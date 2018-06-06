#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
import asyncio

from aiocache.serializers import PickleSerializer
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

from owllook.fetcher.decorators import cached
from owllook.fetcher.function import get_random_user_agent
from owllook.fetcher.novels_factory.base_novels import BaseNovels


class DuckGoNovels(BaseNovels):

    def __init__(self):
        super(DuckGoNovels, self).__init__()

    async def data_extraction(self, html):
        """
        小说信息抓取函数
        :return:
        """
        try:
            title = html.select('h2 a')[0].get_text()
            url = html.select('h2 a')[0].get('href', None)
            url = parse_qs(url).get('uddg', ['#'])[0]
            netloc = urlparse(url).netloc
            url = url.replace('index.html', '').replace('Index.html', '')
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in self.black_domain or '.html' in url:
                return None
            is_parse = 1 if netloc in self.rules.keys() else 0
            is_recommend = 1 if netloc in self.latest_rules.keys() else 0
            # time = html.select('div.b_attribution')[0].get_text()
            # time = re.findall(r'\d+-\d+-\d+', time)
            # time = time[0] if time else ''
            timestamp = 0
            time = ''
            return {'title': title,
                    'url': url,
                    'time': time,
                    'is_parse': is_parse,
                    'is_recommend': is_recommend,
                    'timestamp': timestamp,
                    'netloc': netloc}

        except Exception as e:
            self.logger.exception(e)
            return None

    async def novels_search(self, novels_name):
        """
        小说搜索入口函数
        :return:
        """
        url = self.config.DUCKGO_URL
        headers = {
            'user-agent': await get_random_user_agent(),
            'referer': "https://duckduckgo.com/"
        }
        params = {'q': novels_name}
        html = await self.fetch_url(url=url, params=params, headers=headers)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all(class_='result')
            extra_tasks = [self.data_extraction(html=i) for i in result]
            tasks = [asyncio.ensure_future(i) for i in extra_tasks]
            done_list, pending_list = await asyncio.wait(tasks)
            res = [task.result() for task in done_list if task.result()]
            return res
        else:
            return []


@cached(ttl=259200, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def start(novels_name):
    """
    Start spider
    :return:
    """
    return await DuckGoNovels.start(novels_name)


if __name__ == '__main__':
    # Start
    res = asyncio.get_event_loop().run_until_complete(start('雪中悍刀行 小说 阅读 最新章节'))
    print(res)
