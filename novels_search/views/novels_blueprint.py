#!/usr/bin/env python
import time

from sanic import Blueprint
from sanic.response import redirect, html, text
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import urlparse
from operator import itemgetter

from novels_search.database.mongodb import MotorBase
from novels_search.fetcher.function import get_time
from novels_search.fetcher.cache import cache_owllook_novels_content, cache_owllook_novels_chapter, \
    cache_owllook_baidu_novels_result
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
        return template('index.html', title='owllook - 网络小说搜索引擎', is_login=1, user=user)
    else:
        return template('index.html', title='owllook - 网络小说搜索引擎', is_login=0)


@novels_bp.route("/search", methods=['GET'])
async def owllook_search(request):
    start = time.time()
    name = request.args.get('wd', None)
    motor_db = MotorBase().db
    if not name:
        return redirect('/')
    else:
        novels_name = 'intitle:{name} 小说 阅读'.format(name=name) if ':baidu' not in name else name.split('baidu')[1]
        try:
            motor_db.search_records.update_one({'keyword': name}, {'$inc': {'count': 1}}, upsert=True)
        except Exception as e:
            LOGGER.exception(e)
    # is_web = int(request.args.get('is_web', 1))
    result = await cache_owllook_baidu_novels_result(novels_name)
    if result:
        parse_result = [i for i in result if i]
        # result_sorted = sorted(
        #     parse_result, reverse=True, key=lambda res: res['timestamp']) if ':baidu' not in name else parse_result
        # 优先依靠是否解析进行排序  其次以更新时间进行排序
        result_sorted = sorted(
            parse_result, reverse=True,
            key=itemgetter('is_parse', 'timestamp')) if ':baidu' not in name else parse_result
        user = request['session'].get('user', None)
        if user:
            try:
                time_current = get_time()
                res = motor_db.user_message.update_one({'user': user}, {'$set': {'last_update_time': time_current}},
                                                       upsert=True)
                # 此处语法操作过多  下次看一遍mongo再改
                if res:
                    is_ok = motor_db.user_message.update_one(
                        {'user': user, 'search_records.keyword': {'$ne': name}},
                        {'$push': {'search_records': {'keyword': name, 'counts': 0}}},
                    )

                    if is_ok:
                        motor_db.user_message.update_one(
                            {'user': user, 'search_records.keyword': name},
                            {'$inc': {'search_records.$.counts': 1}}
                        )

            except Exception as e:
                LOGGER.exception(e)
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
        return html("No Result！请将小说名反馈给本站，谢谢！")


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
        content = str(content).strip('[],')
        return template(
            'chapter.html', novels_name=novels_name, url=url, content_url=content_url, soup=content)
    else:
        return text('解析失败，请将失败页面反馈给本站')


@novels_bp.route("/owllook_content")
async def owllook_content(request):
    url = request.args.get('url', None)
    chapter_url = request.args.get('chapter_url', None)
    novels_name = request.args.get('novels_name', None)
    name = request.args.get('name', None)
    bookmark_url = "{path}?url={url}&name={name}&chapter_url={chapter_url}&novels_name={novels_name}".format(
        path=request.url,
        url=url,
        name=name,
        chapter_url=chapter_url,
        novels_name=novels_name
    )
    book_url = "/chapter?url={chapter_url}&novels_name={novels_name}".format(
        chapter_url=chapter_url,
        novels_name=novels_name)
    netloc = urlparse(url).netloc
    if netloc not in RULES.keys():
        return redirect(url)
    content_url = RULES[netloc].content_url
    content = await cache_owllook_novels_content(url=url, netloc=netloc)
    if content:
        user = request['session'].get('user', None)
        # 破坏广告链接
        content = str(content).strip('[]Jjs,').replace('http', 'hs')
        if user:
            motor_db = MotorBase().db
            bookmark = await motor_db.user_message.find_one({'bookmarks.bookmark': bookmark_url})
            book = await motor_db.user_message.find_one({'books_url.book_url': book_url})
            bookmark = 1 if bookmark else 0
            book = 1 if book else 0
            return template(
                'content.html',
                is_login=1,
                user=user,
                name=name,
                url=url,
                bookmark=bookmark,
                book=book,
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
                bookmark=0,
                book=0,
                content_url=content_url,
                chapter_url=chapter_url,
                novels_name=novels_name,
                soup=content)
    else:
        return text('解析失败，请将失败页面反馈给本站')


@novels_bp.route("/register")
async def owllook_register(request):
    """
    用户登录
    :param request:
    :return:
        :   -1  用户名或密码不能为空
        :   0   用户名或密码错误
        :   1   登陆成功
    """
    user = request['session'].get('user', None)
    # cookies = request.cookies.get('user')
    # print(cookies)
    if user:
        return redirect('/')
    else:
        return template('register.html', title='owllook - 注册 - 网络小说搜索引擎')


@novels_bp.route("/owllook_donate")
async def donate(request):
    return template('donate.html')


@novels_bp.route("/owllook_feedback")
async def feedback(request):
    return template('feedback.html')
