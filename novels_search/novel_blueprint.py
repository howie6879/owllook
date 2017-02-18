#!/usr/bin/env python
from sanic import Blueprint
from sanic.response import redirect, json, html
from sanic.exceptions import ServerError
from jinja2 import Environment, PackageLoader, select_autoescape
from novels_search.fetcher.novels import search
import time

bp = Blueprint('novel_blueprint')
bp.static('/static', './static')
env = Environment(loader=PackageLoader('novel_blueprint', 'template'),
                  autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


@bp.route("/")
async def index(request):
    return template('index.html', title='index')


@bp.route("/search", methods=['GET'])
async def donate(request):
    start = time.time()
    name = request.args.get('wd', None)
    if not name:
        return redirect('/')
    else:
        name = '{name} 小说 阅读'.format(name=name)
    is_web = int(request.args.get('is_web', 1))
    result = await search(name, is_web)
    parse_result = [i for i in result if i]
    return template('result.html', title=name + '-搜索结果', time=time.time() - start, result=parse_result)


@bp.route("/donate")
async def donate(request):
    return template('donate.html')


@bp.route("/feedback")
async def feedback(request):
    return template('feedback.html')


@bp.exception(ServerError)
async def test(request, exception):
    return json({"exception": "{}".format(exception), "status": exception.status_code}, status=exception.status_code)
