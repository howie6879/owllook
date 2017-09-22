#!/usr/bin/env python
from functools import wraps
from sanic.request import Request
from sanic import response

try:
    from ujson import loads as json_loads
    from ujson import dumps as json_dumps
except:
    from json import loads as json_loads
    from json import dumps as json_dumps

from owllook.fetcher import UniResponse
from owllook.config import CONFIG, LOGGER


def response_handle(request, dict_value, status=200):
    """
    Return sanic.response or json depending on the request
    :param request: sanic.request.Request or dict
    :param dict_value:
    :return:
    """
    if isinstance(request, Request):
        return response.json(dict_value, status=status)
    else:
        return json_dumps(dict_value, ensure_ascii=False)


def authenticator(key):
    """
    
    :param keys: 验证方式 Owllook-Api-Key : Magic Key,  Authorization : Token
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
                return response_handle(request, UniResponse.NOT_AUTHORIZED, status=401)

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
            request_params = {}
            # POST request
            if request.method == 'POST' or request.method == 'DELETE':
                try:
                    post_data = json_loads(str(request.body, encoding='utf-8'))
                except Exception as e:
                    LOGGER.exception(e)
                    return response_handle(request, UniResponse.PARAM_PARSE_ERR, status=400)
                else:
                    request_params.update(post_data)
                    params = [key for key, value in post_data.items() if value]
            elif request.method == 'GET':
                request_params.update(request.args)
                params = [key for key, value in request.args.items() if value]
            else:
                # TODO
                return response_handle(request, UniResponse.PARAM_UNKNOWN_ERR, status=400)
            if set(keys).issubset(set(params)):
                try:
                    kwargs['request_params'] = request_params
                    response = await func(request, *args, **kwargs)
                    return response
                except Exception as e:
                    LOGGER.exception(e)
                    return response_handle(request, UniResponse.SERVER_UNKNOWN_ERR, 500)
            else:
                return response_handle(request, UniResponse.PARAM_ERR, status=400)

        return auth_param

    return wrapper
