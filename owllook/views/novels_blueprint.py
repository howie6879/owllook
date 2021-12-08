#!/usr/bin/env python
import time

from jinja2 import Environment, PackageLoader, select_autoescape
from operator import itemgetter
from sanic import Blueprint
from sanic.response import redirect, html, text, json

from owllook.config import RULES, LOGGER, REPLACE_RULES, ENGINE_PRIORITY, CONFIG
from owllook.database.mongodb import MotorBase
from owllook.fetcher.cache import cache_owllook_novels_content, cache_owllook_novels_chapter, \
    cache_owllook_search_ranking
from owllook.fetcher.function import get_time, get_netloc
from owllook.fetcher.novels_tools import get_novels_info
from owllook.utils import ver_question

novels_bp = Blueprint('novels_blueprint')
novels_bp.static('/static/novels', CONFIG.BASE_DIR + '/static/novels')


@novels_bp.listener('before_server_start')
def setup_db(novels_bp, loop):
    global motor_base
    motor_base = MotorBase()


@novels_bp.listener('after_server_stop')
def close_connection(novels_bp, loop):
    motor_base = None


# jinjia2 config
env = Environment(
    loader=PackageLoader('owllook.views.novels_blueprint', '../templates/novels'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


@novels_bp.route("/chapter")
async def chapter(request):
    """
    返回小说章节目录页
    : content_url   这决定当前U页面url的生成方式
    : url           章节目录页源url
    : novels_name   小说名称
    :return: 小说章节内容页
    """
    url = request.args.get('url', None)
    novels_name = request.args.get('novels_name', None)
    netloc = get_netloc(url)
    if netloc not in RULES.keys():
        return redirect(url)
    if netloc in REPLACE_RULES.keys():
        url = url.replace(REPLACE_RULES[netloc]['old'], REPLACE_RULES[netloc]['new'])
    content_url = RULES[netloc].content_url
    content = await cache_owllook_novels_chapter(url=url, netloc=netloc)
    if content:
        content = str(content).strip('[],, Jjs').replace(', ', '').replace('onerror', '').replace('js', '').replace(
            '加入书架', '')
        return template(
            'chapter.html', novels_name=novels_name, url=url, content_url=content_url, soup=content)
    else:
        return text('解析失败，请将失败页面反馈给本站，请重新刷新一次，或者访问源网页：{url}'.format(url=url))


@novels_bp.route("/owllook_donate")
async def donate(request):
    return template('donate.html')


@novels_bp.route("/owllook_feedback")
async def feedback(request):
    return template('feedback.html')


@novels_bp.route("/")
async def index(request):
    user = request['session'].get('user', None)
    search_ranking = await cache_owllook_search_ranking()
    if user:
        return template('index.html', title='owllook - 网络小说搜索引擎', is_login=1, user=user,
                        search_ranking=search_ranking[:25])
    else:
        return template('index.html', title='owllook - 网络小说搜索引擎', is_login=0, search_ranking=search_ranking[:25])


@novels_bp.route("/owllook_content")
async def owllook_content(request):
    """
    返回小说章节内容页
    : content_url   这决定当前U页面url的生成方式
    : url           章节内容页源url
    : chapter_url   小说目录源url
    : novels_name   小说名称
    :return: 小说章节内容页
    """
    url = request.args.get('url', None)
    chapter_url = request.args.get('chapter_url', None)
    novels_name = request.args.get('novels_name', None)
    name = request.args.get('name', '')
    is_ajax = request.args.get('is_ajax', '')
    # 当小说内容url不在解析规则内 跳转到原本url
    netloc = get_netloc(url)
    if netloc not in RULES.keys():
        return redirect(url)
    user = request['session'].get('user', None)
    # 拼接小说目录url
    book_url = "/chapter?url={chapter_url}&novels_name={novels_name}".format(
        chapter_url=chapter_url,
        novels_name=novels_name)
    motor_db = motor_base.get_db()
    if url == chapter_url:
        # 阅读到最后章节时候 在数据库中保存最新阅读章节
        if user and is_ajax == "owl_cache":
            owl_referer = request.headers.get('Referer', '').split('owllook_content')[1]
            if owl_referer:
                latest_read = "/owllook_content" + owl_referer
                await motor_db.user_message.update_one(
                    {'user': user, 'books_url.book_url': book_url},
                    {'$set': {'books_url.$.last_read_url': latest_read}})
        return redirect(book_url)
    content_url = RULES[netloc].content_url
    content_data = await cache_owllook_novels_content(url=url, chapter_url=chapter_url,netloc=netloc)
    if content_data:
        try:
            content = content_data.get('content', '获取失败')
            next_chapter = content_data.get('next_chapter', [])
            title = content_data.get('title', '').replace(novels_name, '')
            name = title if title else name
            # 拼接小说书签url
            bookmark_url = "{path}?url={url}&name={name}&chapter_url={chapter_url}&novels_name={novels_name}".format(
                path=request.path,
                url=url,
                name=name,
                chapter_url=chapter_url,
                novels_name=novels_name
            )
            # 破坏广告链接
            content = str(content).strip('[]Jjs,').replace('http', 'hs').replace('.js', '').replace('();', '')
            content += """欢迎关注公众号【粮草小说】，享受精品书籍推荐以及实体书赠送福利！"""
            if user:
                bookmark = await motor_db.user_message.find_one({'user': user, 'bookmarks.bookmark': bookmark_url})
                book = await motor_db.user_message.find_one({'user': user, 'books_url.book_url': book_url})
                bookmark = 1 if bookmark else 0
                if book:
                    # 当书架中存在该书源
                    book = 1
                    # 保存最后一次阅读记录
                    if is_ajax == "owl_cache":
                        owl_referer = request.headers.get('Referer', bookmark_url).split('owllook_content')[1]
                        latest_read = "/owllook_content" + owl_referer
                        await motor_db.user_message.update_one(
                            {'user': user, 'books_url.book_url': book_url},
                            {'$set': {'books_url.$.last_read_url': latest_read}})
                else:
                    book = 0
                if is_ajax == "owl_cache":
                    owl_cache_dict = dict(
                        is_login=1,
                        user=user,
                        name=name,
                        url=url,
                        bookmark=bookmark,
                        book=book,
                        content_url=content_url,
                        chapter_url=chapter_url,
                        novels_name=novels_name,
                        next_chapter=next_chapter,
                        soup=content
                    )
                    return json(owl_cache_dict)
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
                    next_chapter=next_chapter,
                    soup=content)
            else:
                if is_ajax == "owl_cache":
                    owl_cache_dict = dict(
                        is_login=0,
                        name=name,
                        url=url,
                        bookmark=0,
                        book=0,
                        content_url=content_url,
                        chapter_url=chapter_url,
                        novels_name=novels_name,
                        next_chapter=next_chapter,
                        soup=content
                    )
                    return json(owl_cache_dict)
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
                    next_chapter=next_chapter,
                    soup=content)
        except Exception as e:
            LOGGER.exception(e)
            return redirect(book_url)
    else:
        if user:
            is_login = 1
            user = user
            return template('parse_error.html', url=url, is_login=is_login, user=user)
        else:
            is_login = 0
            return template('parse_error.html', url=url, is_login=is_login)


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
    if user:
        return redirect('/')
    else:
        ver_que_ans = ver_question()
        if ver_que_ans:
            request['session']['index'] = ver_que_ans
            return template(
                'register.html',
                title='owllook - 注册 - 网络小说搜索引擎',
                question=ver_que_ans[1]
            )
        else:
            return redirect('/')


@novels_bp.route("/search", methods=['GET'])
async def owllook_search(request):
    start = time.time()
    name = str(request.args.get('wd', '')).strip()
    novels_keyword = name.split(' ')[0]
    motor_db = motor_base.get_db()
    if not name:
        return redirect('/')
    else:
        # 记录搜索小说名
        try:
            await motor_db.search_records.update_one({'keyword': name}, {'$inc': {'count': 1}}, upsert=True)
        except Exception as e:
            LOGGER.exception(e)
    # 通过搜索引擎获取检索结果
    parse_result = None
    if name.startswith('!baidu'):
        novels_keyword = name.split('baidu')[1].strip()
        novels_name = 'intitle:{name} 小说 阅读'.format(name=novels_keyword)
        parse_result = await get_novels_info(class_name='baidu', novels_name=novels_name)
    elif name.startswith('!360'):
        novels_keyword = name.split('360')[1].strip()
        novels_name = "{name} 小说 最新章节".format(name=novels_keyword)
        parse_result = await get_novels_info(class_name='so', novels_name=novels_name)
    elif name.startswith('!bing'):
        novels_keyword = name.split('bing')[1].strip()
        novels_name = "{name} 小说 阅读 最新章节".format(name=novels_keyword)
        parse_result = await get_novels_info(class_name='bing', novels_name=novels_name)
    elif name.startswith('!duck_go'):
        novels_keyword = name.split('duck_go')[1].strip()
        novels_name = '{name} 小说 阅读 最新章节'.format(name=novels_keyword)
        parse_result = await get_novels_info(class_name='duck_go', novels_name=novels_name)
    else:
        for each_engine in ENGINE_PRIORITY:
            # for bing
            if each_engine == "bing":
                novels_name = "{name} 小说 阅读 最新章节".format(name=name)
                parse_result = await get_novels_info(class_name='bing', novels_name=novels_name)
                if parse_result:
                    break
            # for 360 so
            if each_engine == "360":
                novels_name = "{name} 小说 最新章节".format(name=name)
                parse_result = await get_novels_info(class_name='so', novels_name=novels_name)
                if parse_result:
                    break
            # for baidu
            if each_engine == "baidu":
                novels_name = 'intitle:{name} 小说 阅读'.format(name=name)
                parse_result = await get_novels_info(class_name='baidu', novels_name=novels_name)
                if parse_result:
                    break
            # for duckduckgo
            if each_engine == "duck_go":
                novels_name = '{name} 小说 阅读 最新章节'.format(name=name)
                parse_result = await get_novels_info(class_name='duck_go', novels_name=novels_name)
                if parse_result:
                    break
    if parse_result:
        # result_sorted = sorted(
        #     parse_result, reverse=True, key=lambda res: res['timestamp']) if ':baidu' not in name else parse_result
        # 优先依靠是否解析进行排序  其次以更新时间进行排序
        result_sorted = sorted(
            parse_result,
            reverse=True,
            key=itemgetter('is_recommend', 'is_parse', 'timestamp'))
        user = request['session'].get('user', None)
        if user:
            try:
                time_current = get_time()
                res = await motor_db.user_message.update_one({'user': user},
                                                             {'$set': {'last_update_time': time_current}},
                                                             upsert=True)
                # 此处语法操作过多  下次看一遍mongo再改
                if res:
                    is_ok = await motor_db.user_message.update_one(
                        {'user': user, 'search_records.keyword': {'$ne': novels_keyword}},
                        {'$push': {'search_records': {'keyword': novels_keyword, 'counts': 1}}},
                    )

                    if is_ok:
                        await motor_db.user_message.update_one(
                            {'user': user, 'search_records.keyword': novels_keyword},
                            {'$inc': {'search_records.$.counts': 1}}
                        )

            except Exception as e:
                LOGGER.exception(e)
            return template(
                'result.html',
                is_login=1,
                user=user,
                name=novels_keyword,
                time='%.2f' % (time.time() - start),
                result=result_sorted,
                count=len(parse_result))

        else:
            return template(
                'result.html',
                is_login=0,
                name=novels_keyword,
                time='%.2f' % (time.time() - start),
                result=result_sorted,
                count=len(parse_result))

    else:
        return html("No Result！请将小说名反馈给本站，谢谢！")
