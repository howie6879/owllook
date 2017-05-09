#!/usr/bin/env python
from sanic import Blueprint, response
from urllib.parse import unquote
from bs4 import BeautifulSoup
from pprint import pprint

from novels_search.fetcher.function import get_time, get_netloc
from novels_search.fetcher.extract_novels import extract_chapters
from novels_search.fetcher.decorators import authenticator, auth_params
from novels_search.fetcher.cache import cache_owllook_baidu_novels_result, cache_owllook_so_novels_result, \
    cache_owllook_novels_chapter
from novels_search.config import LOGGER

api_bp = Blueprint('api_blueprint', url_prefix='v1')


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
        parse_result = None
        if res:
            parse_result = [i for i in res if i]
            result = {'status': 200}
        else:
            result = {'status': 204}
        result.update({'data': parse_result, 'msg': "ok"})
    except Exception as e:
        LOGGER.exception(e)
        result = {'status': 500, 'msg': e}
    result.update({'finished_at': get_time()})
    return response.json(result)


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
        parse_result = None
        if res:
            parse_result = [i for i in res if i]
            result = {'status': 200}
        else:
            result = {'status': 204}
        result.update({'data': parse_result, 'msg': "ok"})
    except Exception as e:
        LOGGER.exception(e)
        result = {'status': 500, 'msg': e}
    result.update({'finished_at': get_time()})
    return response.json(result)


@api_bp.route("/owl_novels_chapters")
@auth_params('chapters_url', 'novels_name')
@authenticator('Owllook-Api-Key')
async def owl_novels_chapters(request):
    """
    返回章节目录 基本达到通用
    :param request: 
    :param chapter_url: 章节源目录页url
    :param novels_name: 小说名称
    :return: 小说目录信息
    """
    chapters_url = request.args.get('chapters_url', None)
    novels_name = request.args.get('novels_name', None)
    netloc = get_netloc(chapters_url)
    try:
        res = await cache_owllook_novels_chapter(url=chapters_url, netloc=netloc)
        chapters_sorted = []
        if res:
            chapters_sorted = extract_chapters(chapters_url, res)
            result = {'status': 200}
        else:
            result = {'status': 204}
        result.update({
            'data': {
                'novels_name': novels_name,
                'chapter_url': chapters_url,
                'all_chapters': chapters_sorted
            },
            'msg': "ok"})
    except Exception as e:
        LOGGER.exception(e)
        result = {'status': 500, 'msg': e}
    result.update({'finished_at': get_time()})
    return response.json(result)
