#!/usr/bin/env python
import aiohttp
import async_timeout
import re

from aiocache.serializers import PickleSerializer
from aiocache.utils import get_args_dict, get_cache
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

from owllook.database.mongodb import MotorBase
from owllook.fetcher import baidu_search, so_search, bing_search, duck_search
from owllook.fetcher.function import target_fetch, get_time, requests_target_fetch
from owllook.fetcher.extract_novels import extract_pre_next_chapter
from owllook.config import RULES, LATEST_RULES, LOGGER


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
                LOGGER.exception("Unexpected error with %s", cache_instance)

            result = await func(*args, **kwargs)
            if result:
                try:
                    await cache_instance.set(cache_key, result, ttl=ttl)
                except Exception:
                    LOGGER.exception("Unexpected error with %s", cache_instance)

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
            if content:
                # 提取出真正的章节标题
                title_reg = r'(第?\s*[一二两三四五六七八九十○零百千万亿0-9１２３４５６７８９０]{1,6}\s*[章回卷节折篇幕集]\s*.*?)[_,-]'
                title = soup.title.string
                extract_title = re.findall(title_reg, title, re.I)
                if extract_title:
                    title = extract_title[0]
                else:
                    title = soup.select('h1')[0].get_text()
                if not title:
                    title = soup.title.string
                # if "_" in title:
                #     title = title.split('_')[0]
                # elif "-" in title:
                #     title = title.split('-')[0]
                next_chapter = extract_pre_next_chapter(chapter_url=url, html=str(soup))
                content = [str(i) for i in content]
                data = {
                    'content': ''.join(content),
                    'next_chapter': next_chapter,
                    'title': title
                }
            else:
                data = None
            return data
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


@cached(ttl=259200, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def cache_owllook_baidu_novels_result(novels_name):
    result = await baidu_search(novels_name)
    parse_result = [i for i in result if i]
    return parse_result if parse_result else None


@cached(ttl=259200, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def cache_owllook_so_novels_result(novels_name):
    result = await so_search(novels_name)
    parse_result = [i for i in result if i]
    return parse_result if parse_result else None


@cached(ttl=259200, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def cache_owllook_bing_novels_result(novels_name):
    result = await bing_search(novels_name)
    parse_result = [i for i in result if i]
    return parse_result if parse_result else None


@cached(ttl=259200, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def cache_owllook_duck_novels_result(novels_name):
    result = await duck_search(novels_name)
    parse_result = [i for i in result if i]
    return parse_result if parse_result else None


@cached(ttl=10800, key_from_attr='search_ranking', serializer=PickleSerializer(), namespace="ranking")
async def cache_owllook_search_ranking():
    motor_db = MotorBase().get_db()
    keyword_cursor = motor_db.search_records.find(
        {'count': {'$gte': 50}},
        {'keyword': 1, 'count': 1, '_id': 0}
    ).sort('count', -1).limit(35)
    result = []
    index = 1
    async for document in keyword_cursor:
        result.append({'keyword': document['keyword'], 'count': document['count'], 'index': index})
        index += 1
    return result


@cached(ttl=3600, key_from_attr='search_ranking', serializer=PickleSerializer(), namespace="ranking")
async def cache_others_search_ranking(spider='qidian', novel_type='全部类别'):
    motor_db = MotorBase().get_db()
    item_data = await motor_db.novels_ranking.find_one({'spider': spider, 'type': novel_type}, {'data': 1, '_id': 0})
    return item_data


async def get_the_latest_chapter(chapter_url, loop=None):
    try:
        with async_timeout.timeout(30):
            url = parse_qs(urlparse(chapter_url).query).get('url', '')
            novels_name = parse_qs(urlparse(chapter_url).query).get('novels_name', '')
            data = None
            if url and novels_name:
                url = url[0]
                novels_name = novels_name[0]
                netloc = urlparse(url).netloc
                if netloc in LATEST_RULES.keys():
                    async with aiohttp.ClientSession(loop=loop) as client:
                        try:
                            html = await target_fetch(client=client, url=url)
                            if html is None:
                                html = requests_target_fetch(url=url)
                        except TypeError:
                            html = requests_target_fetch(url=url)
                        except Exception as e:
                            LOGGER.exception(e)
                            return None
                        try:
                            soup = BeautifulSoup(html, 'html5lib')
                        except Exception as e:
                            LOGGER.exception(e)
                            return None
                        latest_chapter_name, latest_chapter_url = None, None
                        if LATEST_RULES[netloc].plan:
                            meta_value = LATEST_RULES[netloc].meta_value
                            latest_chapter_name = soup.select(
                                'meta[property="{0}"]'.format(meta_value["latest_chapter_name"]))
                            latest_chapter_name = latest_chapter_name[0].get('content',
                                                                             None) if latest_chapter_name else None
                            latest_chapter_url = soup.select(
                                'meta[property="{0}"]'.format(meta_value["latest_chapter_url"]))
                            latest_chapter_url = urljoin(url, latest_chapter_url[0].get('content',
                                                                                        None)) if latest_chapter_url else None
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
                                    # TODO
                                    pass
                                elif content_url == '0':
                                    # TODO
                                    pass
                                else:
                                    latest_chapter_url = content_url + latest_chapter_soup[0].get('href', None)
                                latest_chapter_name = latest_chapter_soup[0].get('title', None)
                        if latest_chapter_name and latest_chapter_url:
                            time_current = get_time()
                            print(latest_chapter_url)
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
                            motor_db = MotorBase().get_db()
                            await motor_db.latest_chapter.update_one(
                                {"novels_name": novels_name, 'owllook_chapter_url': chapter_url},
                                {'$set': {'data': data, "finished_at": time_current}}, upsert=True)
            return data
    except Exception as e:
        LOGGER.exception(e)
        return None


async def update_all_books(loop):
    try:
        motor_db = MotorBase().get_db()
        # 获取所有书架链接游标
        books_url_cursor = motor_db.user_message.find({}, {'books_url.book_url': 1, '_id': 0})
        book_urls = []
        already_urls = set()
        async for document in books_url_cursor:
            if document:
                books_url = document['books_url']

                for book_url in books_url:
                    chapter_url = book_url['book_url']
                    if chapter_url not in already_urls:
                        try:
                            with async_timeout.timeout(30):
                                await get_the_latest_chapter(chapter_url, loop)
                        except Exception as e:
                            LOGGER.exception(e)
                        already_urls.add(chapter_url)
                        # 一组书架链接列表数据
                        #         book_urls += [book_url['book_url'] for book_url in books_url]
                        # url_tasks = [get_the_latest_chapter(each_url, loop) for each_url in set(book_urls)]
                        # tasks = [asyncio.ensure_future(i) for i in url_tasks]
                        # try:
                        #     await asyncio.gather(*tasks)
                        # except asyncio.TimeoutError as e:
                        #     pass
    except Exception as e:
        LOGGER.exception(e)
        return False
