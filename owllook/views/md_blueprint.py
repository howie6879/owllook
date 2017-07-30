#!/usr/bin/env python
from sanic import Blueprint
from sanic.response import html, text, redirect
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import urlparse, parse_qs

from owllook.database.mongodb import MotorBase
from owllook.fetcher.cache import get_the_latest_chapter
from owllook.config import RULES, LOGGER, REPLACE_RULES, ENGINE_PRIORITY, CONFIG

md_bp = Blueprint('rank_blueprint', url_prefix='md')
md_bp.static('/static/md', CONFIG.BASE_DIR + '/static/md')


@md_bp.listener('before_server_start')
def setup_db(rank_bp, loop):
    global motor_base
    motor_base = MotorBase()


@md_bp.listener('after_server_stop')
def close_connection(rank_bp, loop):
    motor_base = None


# jinjia2 config
env = Environment(
    loader=PackageLoader('views.md_blueprint', '../templates/md'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


@md_bp.route("/")
async def index(request):
    user = request['session'].get('user', None)
    if user:
        # motor_db = motor_base.db
        # ranking_cursor = motor_db.novels_ranking.find({})
        # async for document in ranking_cursor:
        #     LOGGER.info(document)
        return template('index.html', title='owllook')
    else:
        return text('请先登录! www.owllook.net')


@md_bp.route("/setting")
async def admin_setting(request):
    user = request['session'].get('user', None)
    if user:
        try:
            return template('admin_setting.html', title='{user}的设置 - owllook'.format(user=user),
                            is_login=1,
                            user=user)
        except Exception as e:
            LOGGER.error(e)
            return redirect('/')
    else:
        return redirect('/')


@md_bp.route("/similar_user")
async def similar_user(request):
    user = request['session'].get('user', None)
    if user:
        try:
            motor_db = motor_base.db
            similar_info = await motor_db.user_recommend.find_one({'user': user})
            if similar_info:
                similar_user = similar_info['similar_user'][:20]
                user_tag = similar_info['user_tag']
                updated_at = similar_info['updated_at']
                return template('similar_user.html',
                                title='与' + user + '相似的书友',
                                is_login=1,
                                is_similar=1,
                                user=user,
                                similar_user=similar_user,
                                user_tag=user_tag,
                                updated_at=updated_at)
            else:
                return template('similar_user.html',
                                title='与' + user + '相似的书友',
                                is_login=1,
                                is_similar=0,
                                user=user)
        except Exception as e:
            LOGGER.error(e)
            return redirect('/')
    else:
        return redirect('/')


@md_bp.route("/books")
async def books(request):
    user = request['session'].get('user', None)
    if user:
        try:
            motor_db = motor_base.db
            data = await motor_db.user_message.find_one({'user': user})
            if data:
                books_url = data.get('books_url', None)
                if books_url:
                    result = []
                    for i in books_url:
                        item_result = {}
                        book_url = i.get('book_url', None)
                        last_read_url = i.get("last_read_url", "")
                        book_query = parse_qs(urlparse(book_url).query)
                        last_read_chapter_name = parse_qs(last_read_url).get('name', ['暂无'])[0]
                        item_result['novels_name'] = book_query.get('novels_name', '')[0] if book_query.get(
                            'novels_name', '') else ''
                        item_result['book_url'] = book_url
                        latest_data = await motor_db.latest_chapter.find_one({'owllook_chapter_url': book_url})
                        if latest_data:
                            item_result['latest_chapter_name'] = latest_data['data']['latest_chapter_name']
                            item_result['owllook_content_url'] = latest_data['data']['owllook_content_url']
                        else:
                            get_latest_data = await get_the_latest_chapter(book_url) or {}
                            item_result['latest_chapter_name'] = get_latest_data.get('latest_chapter_name', '暂未获取，请反馈')
                            item_result['owllook_content_url'] = get_latest_data.get('owllook_content_url', '')
                        item_result['add_time'] = i.get('add_time', '')
                        item_result["last_read_url"] = last_read_url if last_read_url else book_url
                        item_result["last_read_chapter_name"] = last_read_chapter_name
                        result.append(item_result)
                    return template('admin_books.html', title='{user}的书架 - owllook'.format(user=user),
                                    is_login=1,
                                    user=user,
                                    is_bookmark=1,
                                    result=result[::-1])
            return template('admin_books.html', title='{user}的书架 - owllook'.format(user=user),
                            is_login=1,
                            user=user,
                            is_bookmark=0)
        except Exception as e:
            LOGGER.error(e)
            return redirect('/')
    else:
        return redirect('/')


@md_bp.route("/book_list")
async def book_list(request):
    user = request['session'].get('user', None)
    if user:
        try:
            return template('admin_book_list.html', title='{user}的书单 - owllook'.format(user=user),
                            is_login=1,
                            user=user)
        except Exception as e:
            LOGGER.error(e)
            return redirect('/')
    else:
        return redirect('/')


@md_bp.route("/bookmarks")
async def bookmarks(request):
    user = request['session'].get('user', None)
    if user:
        try:
            motor_db = motor_base.db
            data = await motor_db.user_message.find_one({'user': user})
            if data:
                # 获取所有书签
                bookmarks = data.get('bookmarks', None)
                if bookmarks:
                    result = []
                    for i in bookmarks:
                        item_result = {}
                        bookmark = i.get('bookmark', None)
                        query = parse_qs(urlparse(bookmark).query)
                        item_result['novels_name'] = query.get('novels_name', '')[0] if query.get('novels_name',
                                                                                                  '') else ''
                        item_result['chapter_name'] = query.get('name', '')[0] if query.get('name', '') else ''
                        item_result['chapter_url'] = query.get('chapter_url', '')[0] if query.get('chapter_url',
                                                                                                  '') else ''
                        item_result['bookmark'] = bookmark
                        item_result['add_time'] = i.get('add_time', '')
                        result.append(item_result)
                    return template('admin_bookmarks.html', title='{user}的书签 - owllook'.format(user=user),
                                    is_login=1,
                                    user=user,
                                    is_bookmark=1,
                                    result=result[::-1])
            return template('admin_bookmarks.html', title='{user}的书签 - owllook'.format(user=user),
                            is_login=1,
                            user=user,
                            is_bookmark=0)
        except Exception as e:
            LOGGER.error(e)
            return redirect('/')
    else:
        return redirect('/')
