#!/usr/bin/env python
import async_timeout
import random
import os
import aiohttp
import arrow
import requests
import cchardet

from urllib.parse import urlparse

from owllook.config import LOGGER, CONFIG


def get_data(filename, default='') -> list:
    """
    Get data from a file
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(os.path.dirname(__file__))
    user_agents_file = os.path.join(
        os.path.join(root_folder, 'data'), filename)
    try:
        with open(user_agents_file) as fp:
            data = [_.strip() for _ in fp.readlines()]
    except:
        data = [default]
    return data


def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    return random.choice(get_data('user_agents.txt', CONFIG.USER_AGENT))


def get_time() -> str:
    utc = arrow.utcnow()
    local = utc.to(CONFIG.TIMEZONE)
    time = local.format("YYYY-MM-DD HH:mm:ss")
    return time


def get_netloc(url):
    """
    获取netloc
    :param url: 
    :return:  netloc
    """
    netloc = urlparse(url).netloc
    return netloc or None


async def target_fetch(client, url):
    """
    :param client: aiohttp client
    :param url: target url
    :return: text
    """
    with async_timeout.timeout(30):
        try:
            headers = {'user-agent': get_random_user_agent()}
            async with client.get(url, headers=headers) as response:
                assert response.status == 200
                LOGGER.info('Task url: {}'.format(response.url))
                try:
                    text = await response.text()
                except:
                    try:
                        text = await response.read()
                    except aiohttp.errors.ServerDisconnectedError as e:
                        LOGGER.exception(e)
                        text = None
                return text
        except Exception as e:
            LOGGER.exception(e)
            return None


def requests_target_fetch(url):
    """
    :param url:
    :return:
    """
    try:
        headers = {'user-agent': get_random_user_agent()}
        response = requests.get(url=url, headers=headers, verify=False)
        response.raise_for_status()
        content = response.content
        charset = cchardet.detect(content)
        text = content.decode(charset['encoding'])
        return text
    except Exception as e:
        LOGGER.exception(e)
        return None
