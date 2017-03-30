#!/usr/bin/env python
import aiohttp

from bs4 import BeautifulSoup
from aiocache.serializers import PickleSerializer
from aiocache.log import logger
from aiocache.utils import get_args_dict, get_cache

from novels_search.fetcher.baidu_novels import baidu_search
from novels_search.fetcher.so_novels import so_search
from novels_search.fetcher.function import target_fetch
from novels_search.config import RULES


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


@cached(ttl=86400, key_from_attr='url', serializer=PickleSerializer(), namespace="main")
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


@cached(ttl=86400, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def cache_owllook_baidu_novels_result(novels_name):
    result = await baidu_search(novels_name)
    return result if result else None


@cached(ttl=86400, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def cache_owllook_so_novels_result(novels_name):
    result = await so_search(novels_name)
    return result if result else None
