#!/usr/bin/env python
import aiohttp
import async_timeout
import random
import os

from bs4 import BeautifulSoup
from aiocache.serializers import PickleSerializer
from aiocache.log import logger
from aiocache.utils import get_args_dict, get_cache
from novels_search.config import USER_AGENT, RULES, LOGGER


def get_data(filename, default=''):
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


def get_random_user_agent():
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    return random.choice(get_data('user_agents.txt', USER_AGENT))


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


# Token from https://github.com/argaen/aiocache/blob/master/aiocache/decorators.py
def cached(
        ttl=0, key=None, key_from_attr=None, cache=None, serializer=None, plugins=None, **kwargs):
    """
    Caches the functions return value into a key generated with module_name, function_name and args.

    In some cases you will need to send more args to configure the cache object.
    An example would be endpoint and port for the RedisCache. You can send those args as
    kwargs and they will be propagated accordingly.

    :param ttl: int seconds to store the function call. Default is 0 which means no expiration.
    :param key: str value to set as key for the function return. Takes precedence over
        key_from_attr param. If key and key_from_attr are not passed, it will use module_name
        + function_name + args + kwargs
    :param key_from_attr: arg or kwarg name from the function to use as a key.
    :param cache: cache class to use when calling the ``set``/``get`` operations.
        Default is the one configured in ``aiocache.settings.DEFAULT_CACHE``
    :param serializer: serializer instance to use when calling the ``dumps``/``loads``.
        Default is the one configured in ``aiocache.settings.DEFAULT_SERIALIZER``
    :param plugins: plugins to use when calling the cmd hooks
        Default is the one configured in ``aiocache.settings.DEFAULT_PLUGINS``
    """
    cache_kwargs = kwargs

    def cached_decorator(func):
        async def wrapper(*args, **kwargs):
            cache_instance = get_cache(
                cache=cache, serializer=serializer, plugins=plugins, **cache_kwargs)
            args_dict = get_args_dict(func, args, kwargs)
            cache_key = key or args_dict.get(
                key_from_attr,
                (func.__module__ or 'stub') + func.__name__ + str(args) + str(kwargs))

            try:
                if await cache_instance.exists(cache_key):
                    return await cache_instance.get(cache_key)

            except Exception:
                logger.exception("Unexpected error with %s", cache_instance)

            result = await func(*args, **kwargs)

            if result:
                try:
                    await cache_instance.set(cache_key, result, ttl=ttl)
                except Exception:
                    logger.exception("Unexpected error with %s", cache_instance)

            return result

        return wrapper

    return cached_decorator


@cached(key_from_attr='url', serializer=PickleSerializer(), namespace="main")
async def cache_owllook_novels_content(url, netloc):
    async with aiohttp.ClientSession() as client:
        html = await target_fetch(client=client, url=url)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            selector = RULES[netloc].content_selector
            if selector.get('id', None):
                content = soup.find_all(id=selector['id'])
            elif selector.get('class', None):
                content = soup.find_all(class_=selector['class'])
            else:
                content = soup.find_all(selector.get('tag'))
            return str(content) if content else None
        return None


@cached(ttl=3600, key_from_attr='url', serializer=PickleSerializer(), namespace="main")
async def cache_owllook_novels_chapter(url, netloc):
    async with aiohttp.ClientSession() as client:
        html = await target_fetch(client=client, url=url)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            selector = RULES[netloc].chapter_selector
            if selector.get('id', None):
                content = soup.find_all(id=selector['id'])
            elif selector.get('class', None):
                content = soup.find_all(class_=selector['class'])
            else:
                content = soup.find_all(selector.get('tag'))
            return str(content) if content else None
        return None
