#!/usr/bin/env python
import aiohttp

from bs4 import BeautifulSoup
from aiocache.serializers import PickleSerializer
from aiocache.log import logger
from aiocache.utils import get_args_dict, get_cache
from urllib.parse import urlparse, parse_qs

from novels_search.database.mongodb import MotorBase
from novels_search.fetcher.baidu_novels import baidu_search
from novels_search.fetcher.so_novels import so_search
from novels_search.fetcher.function import target_fetch, get_time
from novels_search.config import RULES, LATEST_RULES, LOGGER


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


@cached(ttl=300, key_from_attr='url', serializer=PickleSerializer(), namespace="main")
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


@cached(ttl=300, key_from_attr='url', serializer=PickleSerializer(), namespace="main")
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
    parse_result = [i for i in result if i]
    return parse_result if parse_result else [None]


@cached(ttl=86400, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def cache_owllook_so_novels_result(novels_name):
    result = await so_search(novels_name)
    parse_result = [i for i in result if i]
    return parse_result if parse_result else [None]


async def get_the_latest_chapter(chapter_url):
    url = parse_qs(urlparse(chapter_url).query).get('url', '')
    novels_name = parse_qs(urlparse(chapter_url).query).get('novels_name', '')
    data = None
    if url and novels_name:
        url = url[0]
        novels_name = novels_name[0]
        netloc = urlparse(url).netloc
        if netloc in LATEST_RULES.keys():
            async with aiohttp.ClientSession() as client:
                html = await target_fetch(client=client, url=url)
                soup = BeautifulSoup(html, 'html5lib')
                latest_chapter_name, latest_chapter_url = None, None
                if LATEST_RULES[netloc].plan:
                    meta_value = LATEST_RULES[netloc].meta_value
                    latest_chapter_name = soup.select('meta[property="{0}"]'.format(meta_value["latest_chapter_name"]))
                    latest_chapter_name = latest_chapter_name[0].get('content', None) if latest_chapter_name else None
                    latest_chapter_url = soup.select('meta[property="{0}"]'.format(meta_value["latest_chapter_url"]))
                    latest_chapter_url = latest_chapter_url[0].get('content', None) if latest_chapter_url else None
                else:
                    selector = LATEST_RULES[netloc].selector
                    content_url = selector.get('content_url')
                    if selector.get('id', None):
                        latest_chapter_soup = soup.find_all(id=selector['id'])
                    elif selector.get('class', None):
                        latest_chapter_soup = soup.find_all(class_=selector['class'])
                    else:
                        latest_chapter_soup = soup.select(selector.get('tag'))
                    if latest_chapter_soup:
                        if content_url == '1':
                            pass
                        elif content_url == '0':
                            pass
                        else:
                            latest_chapter_url = content_url + latest_chapter_soup[0].get('href', None)
                        latest_chapter_name = latest_chapter_soup[0].get('title', None)
                if latest_chapter_name and latest_chapter_url:
                    time_current = get_time()
                    data = {
                        "latest_chapter_name": latest_chapter_name,
                        "latest_chapter_url": latest_chapter_url,
                        "owllook_chapter_url": chapter_url,
                        "owllook_content_url": "/owllook_content?url={latest_chapter_url}&name={name}&chapter_url={chapter_url}&novels_name={novels_name}".format(
                            latest_chapter_url=latest_chapter_url,
                            name=latest_chapter_name,
                            chapter_url=url,
                            novels_name=novels_name,
                        ),
                    }
                    # 存储最新章节
                    motor_db = MotorBase().db
                    await motor_db.latest_chapter.update_one(
                        {"novels_name": novels_name, 'owllook_chapter_url': chapter_url},
                        {'$set': {'data': data, "finished_at": time_current}}, upsert=True)
    return data


async def update_all_books():
    try:
        motor_db = MotorBase().db
        # 获取所有书架链接游标
        books_url_cursor = motor_db.user_message.find({}, {'books_url.book_url': 1, '_id': 0})
        # 已更新url集合
        already_urls = set()
        async for document in books_url_cursor:
            if document:
                books_url = document['books_url']
                # 一组书架链接列表数据
                for book_url in books_url:
                    chapter_url = book_url['book_url']
                    if chapter_url not in already_urls:
                        await get_the_latest_chapter(chapter_url)
                        already_urls.add(chapter_url)
        return True
    except Exception as e:
        LOGGER.exception(e)
        return False
