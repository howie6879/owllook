#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""

from importlib import import_module


async def get_novels_info(class_name, novels_name):
    novels_module = import_module(
        "owllook.fetcher.{}.{}_novels".format('novels_factory', class_name))
    # 获取对应渠道实例化对象
    novels_info = await novels_module.start(novels_name)
    return novels_info


if __name__ == '__main__':
    import asyncio
    import aiocache

    REDIS_DICT = {}
    aiocache.settings.set_defaults(
        class_="aiocache.RedisCache",
        endpoint=REDIS_DICT.get('REDIS_ENDPOINT', 'localhost'),
        port=REDIS_DICT.get('REDIS_PORT', 6379),
        db=REDIS_DICT.get('CACHE_DB', 0),
        password=REDIS_DICT.get('REDIS_PASSWORD', None),
    )

    res = asyncio.get_event_loop().run_until_complete(
        get_novels_info(class_name='baidu', novels_name='intitle:雪中悍刀行 小说 阅读'))
    print(res)
