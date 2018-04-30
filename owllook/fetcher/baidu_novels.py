#!/usr/bin/env python
import aiohttp
import arrow
import asyncio
import async_timeout
import re

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from owllook.fetcher.function import get_random_user_agent
from owllook.config import CONFIG, LOGGER, BLACK_DOMAIN, RULES, LATEST_RULES


async def fetch(client, url, name, is_web):
    with async_timeout.timeout(15):
        try:
            headers = {'user-agent': get_random_user_agent()}
            if is_web:
                params = {'wd': name, 'ie': 'utf-8', 'rn': CONFIG.BAIDU_RN, 'vf_bl': 1}
            else:
                params = {'word': name}
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


async def get_real_url(client, url):
    with async_timeout.timeout(5):
        try:
            headers = {'user-agent': get_random_user_agent()}
            async with client.head(url, headers=headers, allow_redirects=True) as response:
                assert response.status == 200
                LOGGER.info('Parse url: {}'.format(response.url))
                # text = ""
                # try:
                #     text = await response.text()
                # except:
                #     text = await response.read()
                # if text:
                #     print(text)
                #     text = re.findall(r'replace\(\"(.*?)\"\)', str(text))
                #     text = text[0] if text[0] else ""
                url = response.url if response.url else None
                return url
        except Exception as e:
            LOGGER.exception(e)
            return None


async def data_extraction_for_phone(html):
    with async_timeout.timeout(10):
        try:
            # Get title
            data_log = eval(html['data-log'])
            url = data_log.get('mu', None)
            if not url:
                return None
            # Get title
            title = html.find('h3').get_text()
            # Get author and update_time (option)
            novel_mess = html.findAll(class_='c-gap-right-large')
            basic_mess = [i.get_text() for i in novel_mess] if novel_mess else None
            return {'title': title, 'url': url, 'basic_mess': basic_mess}
        except Exception as e:
            LOGGER.exception(e)
            return None


async def data_extraction_for_web(html):
    with async_timeout.timeout(10):
        try:
            url = html.find('a').get('href', None)
            if not url or 'baidu' in url or urlparse(url).netloc in BLACK_DOMAIN:
                return None
            netloc = urlparse(url).netloc
            is_parse = 1 if netloc in RULES.keys() else 0
            title = html.select('font[size="3"]')[0].get_text()
            source = html.select('font[color="#008000"]')[0].get_text()
            time = re.findall(r'\d+-\d+-\d+', source)
            time = time[0] if time else None
            timestamp = 0
            if time:
                try:
                    time_list = [int(i) for i in time.split('-')]
                    timestamp = arrow.get(time_list[0], time_list[1], time_list[2]).timestamp
                except Exception as e:
                    LOGGER.exception(e)
                    timestamp = 0
            return {'title': title, 'url': url.replace('index.html', '').replace('Index.html', ''), 'time': time,
                    'is_parse': is_parse,
                    'timestamp': timestamp,
                    'netloc': netloc}
        except Exception as e:
            LOGGER.exception(e)
            return None


async def data_extraction_for_web_baidu(client, html):
    with async_timeout.timeout(20):
        try:
            url = html.select('h3.t a')[0].get('href', None)
            real_url = await get_real_url(client=client, url=url) if url else None
            if real_url:
                real_str_url = str(real_url)
                netloc = urlparse(real_str_url).netloc
                if "http://" + netloc + "/" == real_str_url:
                    return None
                if 'baidu' in real_str_url or netloc in BLACK_DOMAIN:
                    return None
                is_parse = 1 if netloc in RULES.keys() else 0
                title = html.select('h3.t a')[0].get_text()
                is_recommend = 1 if netloc in LATEST_RULES.keys() else 0
                # time = re.findall(r'\d+-\d+-\d+', source)
                # time = time[0] if time else None
                timestamp = 0
                time = ""
                # if time:
                #     try:
                #         time_list = [int(i) for i in time.split('-')]
                #         timestamp = arrow.get(time_list[0], time_list[1], time_list[2]).timestamp
                #     except Exception as e:
                #         LOGGER.exception(e)
                #         timestamp = 0
                return {'title': title, 'url': real_str_url.replace('index.html', ''), 'time': time,
                        'is_parse': is_parse,
                        'is_recommend': is_recommend,
                        'timestamp': timestamp,
                        'netloc': netloc}
            else:
                return None
        except Exception as e:
            LOGGER.exception(e)
            return None


async def baidu_search(name, is_web=1):
    url = CONFIG.URL_PC if is_web else CONFIG.URL_PHONE
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url, name=name, is_web=is_web)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            if is_web:
                # result = soup.find_all(class_='f')
                result = soup.find_all(class_='result')
                extra_tasks = [data_extraction_for_web_baidu(client=client, html=i) for i in result]
                tasks = [asyncio.ensure_future(i) for i in extra_tasks]
            else:
                result = soup.find_all(class_='result c-result c-clk-recommend')
                extra_tasks = [data_extraction_for_phone(i) for i in result]
                tasks = [asyncio.ensure_future(i) for i in extra_tasks]
            # return await asyncio.gather(*tasks)
            done_list, pending_list = await asyncio.wait(tasks)
            res = []
            for task in done_list:
                res.append(task.result())
            return res


if __name__ == '__main__':
    import time

    start = time.time()
    print(asyncio.get_event_loop().run_until_complete(baidu_search('雪中悍刀行')))
    print(time.time() - start)
