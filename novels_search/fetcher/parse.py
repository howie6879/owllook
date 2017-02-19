#!/usr/bin/env python
import asyncio
import aiohttp
import async_timeout
from bs4 import BeautifulSoup
import chardet
from urllib.parse import urlparse
from pprint import pprint

from novels_search.config import LOGGER, RULES
from novels_search.fetcher.function import get_random_user_agent


async def fetch(client, url):
    with async_timeout.timeout(10):
        try:
            headers = {'user-agent': get_random_user_agent()}
            async with client.get(url, headers=headers) as response:
                assert response.status == 200
                LOGGER.info('Task url: {}'.format(response.url))
                text = await response.text()
                return text
        except Exception as e:
            LOGGER.exception(e)
            return None


async def novels_search(url):
    pprint(url)
    async with aiohttp.ClientSession() as client:
        html = await fetch(client=client, url=url)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            return soup
