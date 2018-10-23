#!/usr/bin/env python
"""
 Created by howie.hu at 2018/10/17.
"""

import asyncio
import random

from ruia import Request

from owllook.config import CONFIG


async def get_proxy_ip(valid: int = 1) -> str:
    # random_server = ['http://0.0.0.0:8662/']
    proxy_server = CONFIG.REMOTE_SERVER.get('proxy_server')
    # proxy_server = random_server[random.randint(0, 1)]
    kwargs = {
        'json': {
            "act_id": 1704,
            "version": "1.0",
            "data": {
                "valid": 1
            }
        }
    }
    res = await Request(url=proxy_server, method='POST', res_type='json', **kwargs).fetch()
    proxy = ''
    if res.status == 200:
        proxy = res.html.get('info').get('proxy')
    return proxy


if __name__ == '__main__':
    print(asyncio.get_event_loop().run_until_complete(get_proxy_ip()))
