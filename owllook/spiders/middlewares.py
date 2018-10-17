#!/usr/bin/env python
"""
 Created by howie.hu at 2018/10/17.
"""

from ruia import Middleware

from owllook.spiders.spider_tools import get_proxy_ip

owl_middleware = Middleware()


@owl_middleware.request
async def add_random_proxy(request):
    request.kwargs.update({'proxy': await update_proxy()})
    request.request_config.update({'RETRY_FUNC': retry_func})


async def update_proxy():
    proxy = await get_proxy_ip()
    if proxy:
        proxy = 'http://' + proxy
    else:
        proxy = None
    return proxy


async def retry_func(request):
    proxy = await update_proxy()
    request.kwargs.update({'proxy': proxy})
    return request
