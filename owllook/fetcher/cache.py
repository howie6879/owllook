#!/usr/bin/env python
"""
 Created by howie.hu.
"""

import re
import aiohttp
import async_timeout

from bs4 import BeautifulSoup
from aiocache.serializers import PickleSerializer,JsonSerializer

from urllib.parse import urlparse, parse_qs, urljoin

from owllook.database.mongodb import MotorBase
from owllook.fetcher.decorators import cached
from owllook.fetcher.function import target_fetch, get_time, get_html_by_requests, get_random_user_agent
from owllook.fetcher.extract_novels import extract_pre_next_chapter
from owllook.config import RULES, LATEST_RULES, LOGGER


@cached(ttl=300, key_from_attr='url', serializer=PickleSerializer(), namespace="main")
async def cache_owllook_novels_content(url, netloc):
    headers = {
        'user-agent': await get_random_user_agent()
    }
    html = await target_fetch(headers=headers, url=url)
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
                'content': str(''.join(content)),
                'next_chapter': next_chapter,
                'title': title
            }
        else:
            data = None
        return data
    return None


# @cached(ttl=300, key_from_attr='url', serializer=PickleSerializer(), namespace="main")
async def cache_owllook_novels_chapter(url, netloc):
    headers = {
        'user-agent': await get_random_user_agent()
    }
    html = await target_fetch(headers=headers, url=url)
    if html:
        soup = BeautifulSoup(html, 'html5lib')
        selector = RULES[netloc].chapter_selector
        if selector.get('id', None):
            content = soup.find_all(id=selector['id'])
        elif selector.get('class', None):
            content = soup.find_all(class_=selector['class'])
        else:
            content = soup.find_all(selector.get('tag'))
        # 防止章节被display:none
        return str(content).replace('style', '') if content else None
    return None


@cached(ttl=10800, key_from_attr='search_ranking', serializer=JsonSerializer(), namespace="ranking")
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


@cached(ttl=3600, key_from_attr='search_ranking', serializer=JsonSerializer(), namespace="ranking")
async def cache_others_search_ranking(spider='qidian', novel_type='全部类别'):
    motor_db = MotorBase().get_db()
    item_data = await motor_db.novels_ranking.find_one({'spider': spider, 'type': novel_type}, {'data': 1, '_id': 0})
    return item_data


async def get_the_latest_chapter(chapter_url, timeout=15):
    try:
        with async_timeout.timeout(timeout):
            url = parse_qs(urlparse(chapter_url).query).get('url', '')
            novels_name = parse_qs(urlparse(chapter_url).query).get('novels_name', '')
            data = None
            if url and novels_name:
                url = url[0]
                novels_name = novels_name[0]
                netloc = urlparse(url).netloc
                if netloc in LATEST_RULES.keys():
                    headers = {
                        'user-agent': await get_random_user_agent()
                    }
                    try:
                        html = await target_fetch(url=url, headers=headers, timeout=timeout)
                        if html is None:
                            html = get_html_by_requests(url=url, headers=headers, timeout=timeout)
                    except TypeError:
                        html = get_html_by_requests(url=url, headers=headers, timeout=timeout)
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
                            'meta[property="{0}"]'.format(meta_value["latest_chapter_name"])) or soup.select(
                            'meta[name="{0}"]'.format(meta_value["latest_chapter_name"]))

                        latest_chapter_name = latest_chapter_name[0].get('content',
                                                                         None) if latest_chapter_name else None
                        latest_chapter_url = soup.select(
                            'meta[property="{0}"]'.format(meta_value["latest_chapter_url"])) or soup.select(
                            'meta[name="{0}"]'.format(meta_value["latest_chapter_url"]))
                        latest_chapter_url = urljoin(chapter_url, latest_chapter_url[0].get('content',
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
                        # print(latest_chapter_url)
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


async def update_all_books(loop, timeout=15):
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
                            await get_the_latest_chapter(chapter_url, timeout)
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
