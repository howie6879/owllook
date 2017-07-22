#!/usr/bin/env python
from functools import wraps
from sanic.response import json
from owllook.config import CONFIG


def authenticator(key):
    """
    
    :param keys: 验证方式 Owllook-Api-Key : Maginc Key,  Authorization : Token
    :return: 返回值
    """

    def wrapper(func):
        @wraps(func)
        async def authenticate(request, *args, **kwargs):
            value = request.headers.get(key, None)
            if value and CONFIG.AUTH[key] == value:
                response = await func(request, *args, **kwargs)
                return response
            else:
                return json({'msg': 'not_authorized', 'status': 401})

        return authenticate

    return wrapper


def auth_params(*keys):
    """
    
    :param keys: 判断必须要有的参数
    :return: 返回值
    """

    def wrapper(func):
        @wraps(func)
        async def auth_param(request, *args, **kwargs):
            params = list(request.args.keys()) + list(kwargs.keys())
            if sorted(keys) == sorted(params):
                response = await func(request, *args, **kwargs)
                return response
            else:
                return json({'msg': 'bad_request', 'status': 400})

        return auth_param

    return wrapper
