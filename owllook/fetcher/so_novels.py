#!/usr/bin/env python
import asyncio
import aiohttp
import async_timeout

from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, parse_qs

from owllook.fetcher.function import get_random_user_agent
from owllook.config import SO_URL, LOGGER, BLACK_DOMAIN, RULES


async def fetch(client, url, novels_name):
    with async_timeout.timeout(15):
        try:
            headers = {'user-agent': get_random_user_agent()}
            params = {'q': novels_name, 'ie': 'utf-8'}
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
            try:
                url = html.select('h3.res-title a')[0].get('href', None)
                title = html.select('h3.res-title a')[0].get_text()
            except IndexError:
                url = html.select('h3.title a')[0].get('href', None)
                title = html.select('h3.title a')[0].get_text()
            except Exception as e:
                LOGGER.exception(e)
                url, title = None, None
                return None

            url = parse_qs(urlparse(url).query).get('url', None)
            url = url[0] if url else None
            netloc = urlparse(url).netloc
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in BLACK_DOMAIN:
                return None
            is_parse = 1 if netloc in RULES.keys() else 0
            time = ''
            timestamp = 0
            return {'title': title, 'url': url.replace('index.html', '').replace('Index.html', ''), 'time': time,
                    'is_parse': is_parse,
                    'timestamp': timestamp,
                    'netloc': netloc}
        except Exception as e:
            LOGGER.exception(e)
            return None


async def so_search(novels_name):
    url = SO_URL
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url, novels_name=novels_name)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            result = soup.find_all(class_='res-list')
            extra_tasks = [data_extraction_for_web_so(client=client, html=i) for i in result]
            tasks = [asyncio.ensure_future(i) for i in extra_tasks]
        return await asyncio.gather(*tasks)
