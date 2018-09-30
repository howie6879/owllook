#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
from functools import wraps

from sanic import response

from aiocache.log import logger
from aiocache.utils import get_args_dict, get_cache
from sanic.request import Request

try:
    from ujson import loads as json_loads
    from ujson import dumps as json_dumps
except:
    from json import loads as json_loads
    from json import dumps as json_dumps

from owllook.fetcher import UniResponse
from owllook.config import CONFIG, LOGGER


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
