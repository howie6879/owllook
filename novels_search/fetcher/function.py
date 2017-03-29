#!/usr/bin/env python
import async_timeout
import random
import os
import arrow

from novels_search.config import USER_AGENT, LOGGER, TIMEZONE


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
    return random.choice(get_data('user_agents.txt', USER_AGENT))


def get_time() -> str:
    utc = arrow.utcnow()
    local = utc.to(TIMEZONE)
    time = local.format("YYYY-MM-DD HH:mm:ss")
    return time


async def target_fetch(client, url):
    """

    :param client: aiohttp client
    :param url: targer url
    :return: text
    """
    with async_timeout.timeout(20):
        try:
            headers = {'user-agent': get_random_user_agent()}
            async with client.get(url, headers=headers) as response:
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
