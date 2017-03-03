#!/usr/bin/env python
import time

from sanic import Blueprint
from sanic.response import redirect, html, text, json
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import urlparse

from novels_search.fetcher.novels import search
from novels_search.database.mongodb import MotorBase
from novels_search.fetcher.function import cache_owllook_novels_content, cache_owllook_novels_chapter
from novels_search.config import RULES, LOGGER

novels_bp = Blueprint('novels_blueprint')
novels_bp.static('/static', './static/novels')

# jinjia2 config
env = Environment(
    loader=PackageLoader('views.novels_blueprint', '../templates/novels'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


@novels_bp.route("/")
async def index(request):
    user = request['session'].get('user', None)
    # cookies = request.cookies.get('user')
    # print(cookies)
    if user:
        return template('index.html', title='index', is_login=1, user=user)
    else:
        return template('index.html', title='index', is_login=0)


@novels_bp.route("/search", methods=['GET'])
async def owllook_search(request):
    start = time.time()
    name = request.args.get('wd', None)
    if not name:
        return redirect('/')
    else:
        novels_name = 'intitle:{name} 小说 阅读'.format(name=name)
        try:
            motor_db = MotorBase().db
            keyword = await motor_db.search_records.find_one({'keyword': name})
            if not keyword:
                await motor_db.search_records.save({'keyword': name, 'count': 1})
            else:
                motor_db.search_records.update_one({'keyword': name}, {'$inc': {'count': 1}})
        except Exception as e:
            LOGGER.exception(e)
    is_web = int(request.args.get('is_web', 1))
    result = await search(novels_name, is_web)
    if result:
        parse_result = [i for i in result if i]
        result_sorted = sorted(
            parse_result, reverse=True, key=lambda res: res['timestamp'])
        user = request['session'].get('user', None)
        if user:
            return template(
                'result.html',
                is_login=1,
                user=user,
                name=name,
                time='%.2f' % (time.time() - start),
                result=result_sorted,
                count=len(parse_result))
        else:
            return template(
                'result.html',
                is_login=0,
                name=name,
                time='%.2f' % (time.time() - start),
                result=result_sorted,
                count=len(parse_result))
    else:
        return html("No Result!")


@novels_bp.route("/chapter")
async def chapter(request):
    url = request.args.get('url', None)
    novels_name = request.args.get('novels_name', None)
    netloc = urlparse(url).netloc
    if netloc not in RULES.keys():
        return redirect(url)
    content_url = RULES[netloc].content_url
    content = await cache_owllook_novels_chapter(url=url, netloc=netloc)
    if content:
        content = str(content).replace('[', '').replace(']', '').replace(',', '')
        return template(
            'chapter.html', novels_name=novels_name, url=url, content_url=content_url, soup=content)
    else:
        return text('failed')


@novels_bp.route("/owllook_content")
async def owllook_content(request):
    url = request.args.get('url', None)
    chapter_url = request.args.get('chapter_url', None)
    novels_name = request.args.get('novels_name', None)
    name = request.args.get('name', None)
    netloc = urlparse(url).netloc
    if netloc not in RULES.keys():
        return redirect(url)
    content_url = RULES[netloc].content_url
    content = await cache_owllook_novels_content(url=url, netloc=netloc)
    if content:
        user = request['session'].get('user', None)
        content = str(content).replace('[', '').replace(']', '')
        if user:
            return template(
                'content.html',
                is_login=1,
                user=user,
                name=name,
                url=url,
                content_url=content_url,
                chapter_url=chapter_url,
                novels_name=novels_name,
                soup=content)
        else:
            return template(
                'content.html',
                is_login=0,
                name=name,
                url=url,
                content_url=content_url,
                chapter_url=chapter_url,
                novels_name=novels_name,
                soup=content)
    else:
        return text('failed')


@novels_bp.route("/owllook_donate")
async def donate(request):
    return template('donate.html')


@novels_bp.route("/owllook_feedback")
async def feedback(request):
    return template('feedback.html')
