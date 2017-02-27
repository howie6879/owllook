#!/usr/bin/env python
import time

from sanic import Blueprint
from sanic.response import redirect, html, text, json
from sanic.exceptions import ServerError
from jinja2 import Environment, PackageLoader, select_autoescape
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from novels_search.fetcher.novels import search
from novels_search.fetcher.function import cache_owllook_novels_content, cache_owllook_novels_chapter
from novels_search.config import RULES

bp = Blueprint('novels_blueprint')

# jinjia2 config
bp.static('/static', './static')
env = Environment(
    loader=PackageLoader('novels_blueprint', 'template'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


@bp.route("/")
async def index(request):
    print(22)
    return template('index.html', title='index')


@bp.route("/search", methods=['GET'])
async def owllook_search(request):
    start = time.time()
    name = request.args.get('wd', None)
    if not name:
        return redirect('/')
    else:
        keyword = 'intitle:{name} 小说 阅读'.format(name=name)
    is_web = int(request.args.get('is_web', 1))
    result = await search(keyword, is_web)
    parse_result = [i for i in result if i]
    result_sorted = sorted(
        parse_result, reverse=True, key=lambda res: res['timestamp'])
    return template(
        'result.html',
        name=name,
        time='%.2f' % (time.time() - start),
        result=result_sorted,
        count=len(parse_result))


@bp.route("/chapter")
async def chapter(request):
    url = request.args.get('url', None)
    name = request.args.get('name', None)
    netloc = urlparse(url).netloc
    if netloc not in RULES.keys():
        return redirect(url)
    content_url = RULES[netloc].content_url
    content = await cache_owllook_novels_chapter(url=url, netloc=netloc)
    if content:
        content = str(content).replace('[', '').replace(']', '')
        return template(
            'chapter.html', name=name, url=url, content_url=content_url, soup=content)
    else:
        return text('failed')


@bp.route("/owllook_content")
async def owllook_content(request):
    url = request.args.get('url', None)
    name = request.args.get('name', None)
    netloc = urlparse(url).netloc
    if netloc not in RULES.keys():
        return redirect(url)
    content_url = RULES[netloc].content_url
    content = await cache_owllook_novels_content(url=url, netloc=netloc)
    if content:
        content = str(content).replace('[', '').replace(']', '')
        return template(
            'content.html',
            name=name,
            url=url,
            content_url=content_url,
            soup=content)
    else:
        return text('failed')


@bp.route("/owllook_donate")
async def donate(request):
    return template('donate.html')


@bp.route("/owllook_feedback")
async def feedback(request):
    return template('feedback.html')


@bp.exception(ServerError)
async def test(request, exception):
    return json(
        {
            "exception": "{}".format(exception),
            "status": exception.status_code
        },
        status=exception.status_code)
