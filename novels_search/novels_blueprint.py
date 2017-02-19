#!/usr/bin/env python
from sanic import Blueprint
from sanic.response import redirect, html, text, json
from sanic.exceptions import ServerError
from jinja2 import Environment, PackageLoader, select_autoescape
import time
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from novels_search.fetcher.novels import search, target_fetch
from novels_search.config import RULES

bp = Blueprint('novels_blueprint')
bp.static('/static', './static')
env = Environment(loader=PackageLoader('novels_blueprint', 'template'),
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
        keyword = 'intitle:{name} 小说 阅读'.format(name=name)
    is_web = int(request.args.get('is_web', 1))
    result = await search(keyword, is_web)
    parse_result = [i for i in result if i]
    return template('result.html', name=name, time='%.2f' % (time.time() - start), result=parse_result,
                    count=len(parse_result))


@bp.route("/list")
async def list(request):
    url = request.args.get('url', None)
    name = request.args.get('name', None)
    netloc = urlparse(url).netloc
    if netloc not in RULES.keys():
        return redirect(url)
    async with aiohttp.ClientSession() as client:
        html = await target_fetch(client=client, url=url)
        if html:
            soup = BeautifulSoup(html, 'html5lib')
            selector = RULES[netloc].list
            list = soup.find_all(class_=selector['class'])
        else:
            return text('解析失败')
    return template('list.html', name=name, soup=list)


@bp.route("/donate")
async def donate(request):
    return template('donate.html')


@bp.route("/feedback")
async def feedback(request):
    return template('feedback.html')


@bp.exception(ServerError)
async def test(request, exception):
    return json({"exception": "{}".format(exception), "status": exception.status_code}, status=exception.status_code)
