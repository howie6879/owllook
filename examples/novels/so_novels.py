#!/usr/bin/env python
import aiohttp
import asyncio
import async_timeout

from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

from owllook.fetcher.function import get_random_user_agent
from owllook.config import CONFIG, LOGGER, BLACK_DOMAIN, RULES, LATEST_RULES


async def fetch(client, url, novels_name):
    with async_timeout.timeout(20):
        try:
            headers = {
                'User-Agent': await get_random_user_agent(),
                'Referer': "http://www.so.com/haosou.html?src=home"
            }
            params = {'ie': 'utf-8', 'src': 'noscript_home', 'shb': 1, 'q': novels_name, }
            async with client.get(url, params=params, headers=headers) as response:
                assert response.status == 200
                LOGGER.info('Task url: {}'.format(response.url))
                try:
                    text = await response.text()
                except:
                    text = await response.read()
                return text
        except Exception as e:
            LOGGER.exception(e)
            return None


async def data_extraction_for_web_so(client, html):
    with async_timeout.timeout(15):
        try:
            # 2017.09.09 修改 更加全面地获取title && url
            try:
                title = html.select('h3 a')[0].get_text()
                url = html.select('h3 a')[0].get('href', None)
            except Exception as e:
                LOGGER.exception(e)
                url, title = None, None
                return None
            # 针对不同的请进行url的提取
            if "www.so.com/link?m=" in url:
                url = html.select('h3 a')[0].get('data-url', None)
            if "www.so.com/link?url=" in url:
                url = parse_qs(urlparse(url).query).get('url', None)
                url = url[0] if url else None

            # try:
            #     url = html.select('h3.res-title a')[0].get('data-url', None)
            #     title = html.select('h3.res-title a')[0].get_text()
            # except IndexError:
            #     url = html.select('h3.title a')[0].get('href', None)
            #     url = parse_qs(urlparse(url).query).get('url', None)
            #     url = url[0] if url else None
            #     title = html.select('h3.title a')[0].get_text()
            # except Exception as e:
            #     LOGGER.exception(e)
            #     url, title = None, None
            #     return None

            # 2017.07.09 此处出现bug url展示形式发生变化 因此对于h3.title a形式依旧不变  但是h3.res-title a则取属性data-url
            # url = parse_qs(urlparse(url).query).get('url', None)
            # url = url[0] if url else None

            netloc = urlparse(url).netloc
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in BLACK_DOMAIN:
                return None
            is_parse = 1 if netloc in RULES.keys() else 0
            is_recommend = 1 if netloc in LATEST_RULES.keys() else 0
            time = ''
            timestamp = 0
            return {'title': title, 'url': url.replace('index.html', '').replace('Index.html', ''), 'time': time,
                    'is_parse': is_parse,
                    'is_recommend': is_recommend,
                    'timestamp': timestamp,
                    'netloc': netloc}
        except Exception as e:
            LOGGER.exception(e)
            return None


async def so_search(novels_name):
    url = CONFIG.SO_URL
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url, novels_name=novels_name)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all(class_='res-list')
            extra_tasks = [data_extraction_for_web_so(client=client, html=i) for i in result]
            tasks = [asyncio.ensure_future(i) for i in extra_tasks]
            return await asyncio.gather(*tasks)
        else:
            return []


if __name__ == '__main__':
    import uvloop
    import time

    from pprint import pprint

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


    def novel_task(name):
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(so_search(name))
        loop.run_until_complete(task)
        return task.result()


    start = time.time()
    result = novel_task('圣墟 小说 阅读 最新章节')
    pprint(result)
    print(time.time() - start)
