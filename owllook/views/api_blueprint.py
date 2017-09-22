#!/usr/bin/env python
from sanic import Blueprint, response
from urllib.parse import unquote

from owllook.fetcher.function import get_time, get_netloc
from owllook.fetcher.extract_novels import extract_chapters
from owllook.fetcher.decorators import authenticator, auth_params, response_handle
from owllook.fetcher import UniResponse, ResponseField
from owllook.fetcher.cache import cache_owllook_baidu_novels_result, cache_owllook_so_novels_result, \
    cache_owllook_novels_chapter
from owllook.config import LOGGER

api_bp = Blueprint('api_blueprint', url_prefix='api')


@api_bp.route("/owl_bd_novels/<name>")
@authenticator('Owllook-Api-Key')
async def owl_bd_novels(request, name):
    """
    百度小说信息接口
    :param request: 
    :param name: 小说名
    :return: 小说相关信息
    """
    name = unquote(name)
    novels_name = 'intitle:{name} 小说 阅读'.format(name=name)
    try:
        res = await cache_owllook_baidu_novels_result(novels_name)
        parse_result = []
        if res:
            parse_result = [i for i in res if i]
        UniResponse.SUCCESS.update({ResponseField.DATA: parse_result, ResponseField.FINISH_AT: get_time()})
        return response_handle(request, UniResponse.SUCCESS, 200)
    except Exception as e:
        LOGGER.exception(e)
        return response_handle(request, UniResponse.SERVER_UNKNOWN_ERR, 500)


@api_bp.route("/owl_so_novels/<name>")
@authenticator('Owllook-Api-Key')
async def owl_so_novels(request, name):
    """
    360小说信息接口
    :param request: 
    :param name: 小说名
    :return: 小说相关信息
    """
    name = unquote(name)
    novels_name = '{name} 小说 免费阅读'.format(name=name)
    try:
        res = await cache_owllook_so_novels_result(novels_name)
        parse_result = []
        if res:
            parse_result = [i for i in res if i]
        UniResponse.SUCCESS.update({ResponseField.DATA: parse_result, ResponseField.FINISH_AT: get_time()})
        return response_handle(request, UniResponse.SUCCESS, 200)
    except Exception as e:
        LOGGER.exception(e)
        return response_handle(request, UniResponse.SERVER_UNKNOWN_ERR, 500)


@api_bp.route("/owl_novels_chapters", methods=['POST'])
@auth_params('chapters_url', 'novels_name')
@authenticator('Owllook-Api-Key')
async def owl_novels_chapters(request, **kwargs):
    """
    返回章节目录 基本达到通用
    :param request: 
    :param chapter_url: 章节源目录页url
    :param novels_name: 小说名称
    :return: 小说目录信息
    """
    request_params = kwargs["request_params"]
    chapters_url = request_params.get('chapters_url', None)
    novels_name = request_params.get('novels_name', None)
    netloc = get_netloc(chapters_url)
    try:
        res = await cache_owllook_novels_chapter(url=chapters_url, netloc=netloc)
        chapters_sorted = []
        if res:
            chapters_sorted = extract_chapters(chapters_url, res)
        UniResponse.SUCCESS.update({ResponseField.DATA: {
            'novels_name': novels_name,
            'chapter_url': chapters_url,
            'all_chapters': chapters_sorted
        }, ResponseField.FINISH_AT: get_time()})
        return response_handle(request, UniResponse.SUCCESS, 200)
    except Exception as e:
        LOGGER.exception(e)
        return response_handle(request, UniResponse.SERVER_UNKNOWN_ERR, 500)
