#!/usr/bin/env python
from functools import wraps
from sanic.response import json
from novels_search.config import AUTH


def authenticator(key):
    """
    
    :param keys: 验证方式 Owllook-Api-Key : Maginc Key,  Authorization : Token
    :return: 返回值
    """

    def wrapper(func):
        @wraps(func)
        async def authenticate(request, *args, **kwargs):
            value = request.headers.get(key, None)
            if value and AUTH[key] == value:
                response = await func(request, *args, **kwargs)
                return response
            else:
                return json({'msg': 'not_authorized', 'status': 403})

        return authenticate

    return wrapper
