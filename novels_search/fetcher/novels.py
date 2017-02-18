#!/usr/bin/env python
import asyncio
import aiohttp
import async_timeout
import re
from bs4 import BeautifulSoup
import arrow
from urllib.parse import urlparse
from pprint import pprint

from novels_search.config import URL_PC, URL_PHONE, LOGGER, USER_AGENT


async def fetch(client, url, name, is_web):
    with async_timeout.timeout(10):
        if is_web:
            params = {'wd': name, 'ie': 'utf-8', 'tn': 'baidulocal', 'rn': 50}
        else:
            params = {'word': name}
        async with client.get(url, params=params) as response:
            assert response.status == 200
            LOGGER.info('Task url: {}'.format(response.url))
            text = await response.text()
            return text


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
            if not url or 'baidu' in url:
                return None
            netloc = urlparse(url).netloc
            title = html.select('font[size="3"]')[0].get_text()
            source = html.select('font[color="#008000"]')[0].get_text()
            time = re.findall(r'\d+-\d+-\d+', source)
            time = time[0] if time else None
            timestamp = 0
            if time:
                time_list = [int(i) for i in time.split('-')]
                timestamp = arrow.get(time_list[0], time_list[1], time_list[2]).timestamp
            return {'title': title, 'url': url, 'time': time, 'timestamp': timestamp, 'netloc': netloc}
        except Exception as e:
            LOGGER.exception(e)
            return None


async def search(name, is_web=1):
    url = URL_PC if is_web else URL_PHONE
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url, name=name, is_web=is_web)
        soup = BeautifulSoup(html, 'html5lib')
        if is_web:
            result = soup.find_all(class_='f')
            extra_tasks = [data_extraction_for_web(i) for i in result]
            tasks = [asyncio.ensure_future(i) for i in extra_tasks]
        else:
            result = soup.find_all(class_='result c-result c-clk-recommend')
            extra_tasks = [data_extraction_for_phone(i) for i in result]
            tasks = [asyncio.ensure_future(i) for i in extra_tasks]
        return await asyncio.gather(*tasks)
