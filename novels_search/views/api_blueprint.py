#!/usr/bin/env python
from sanic import Blueprint, response
from urllib.parse import unquote

from novels_search.fetcher.function import get_time
from novels_search.fetcher.decorators import authenticator
from novels_search.fetcher.cache import cache_owllook_novels_result
from novels_search.config import LOGGER

api_bp = Blueprint('api_blueprint', url_prefix='v1')




@api_bp.route("/novels/<name>")
@authenticator('Owllook-Api-Key')
async def index(request, name):
    """
    小说信息接口
    :param request: 
    :param name: 小说名
    :return: 小说相关信息
    """
    name = unquote(name)
    novels_name = 'intitle:{name} 小说 阅读'.format(name=name)
    try:
        res = await cache_owllook_novels_result(novels_name)
        parse_result = None
        if request:
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
