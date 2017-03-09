#!/usr/bin/env python
import hashlib
import arrow

from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.response import html, json

from novels_search.database.mongodb import MotorBase
from novels_search.config import WEBSITE, TIMEZONE, LOGGER

operate_bp = Blueprint('operate_blueprint', url_prefix='operate')
operate_bp.static('/static', './static/operate')

# jinjia2 config
env = Environment(
    loader=PackageLoader('views.operate_blueprint', '../templates/operate'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


def get_time():
    utc = arrow.utcnow()
    local = utc.to(TIMEZONE)
    time = local.format("YYYY-MM-DD HH:mm:ss")
    return time


@operate_bp.route("/login", methods=['POST'])
async def owllook_login(request):
    """
    用户登录
    :param request:
    :return:
        :   -1  用户名或密码不能为空
        :   0   用户名或密码错误
        :   1   登陆成功
    """
    user = request.args.get('user', None)
    pwd = request.args.get('pwd', None)
    if user and pwd:
        motor_db = MotorBase().db
        data = await motor_db.user.find_one({'user': user})
        if data:
            password = hashlib.md5((WEBSITE["TOKEN"] + pwd).encode("utf-8")).hexdigest()
            if password == data.get('password'):
                request['session']['user'] = user
                # response = json({'status': 1})
                # response.cookies['user'] = user
                return json({'status': 1})
        return json({'status': -1})
    else:
        return json({'status': 0})


@operate_bp.route("/logout", methods=['GET'])
async def owllook_logout(request):
    """
    用户登录
    :param request:
    :return:
        :   0   退出失败
        :   1   退出成功
    """
    user = request['session'].get('user', None)
    if user:
        response = json({'status': 1})
        del response.cookies['session']
        return response
    else:
        return json({'status': 0})


@operate_bp.route("/register", methods=['POST'])
async def owllook_register(request):
    """
    用户注册
    :param request:
    :return:
        :   -1  用户名已存在
        :   0   用户名或密码不能为空
        :   1   注册成功
    """
    user = request.args.get('user', None)
    pwd = request.args.get('pwd', None)
    if user and pwd:
        motor_db = MotorBase().db
        is_exist = await motor_db.user.find_one({'user': user})
        if not is_exist:
            password = hashlib.md5((WEBSITE["TOKEN"] + pwd).encode("utf-8")).hexdigest()
            time = get_time()
            data = {
                "user": user,
                "password": password,
                "register_time": time,
            }
            object_id = await motor_db.user.save(data)
            return json({'object_id': str(object_id)}) if object_id else None
        else:
            return json({'status': -1})
    else:
        return json({'status': 0})


@operate_bp.route("/add_bookmark", methods=['POST'])
async def owllook_add_bookmark(request):
    """

    :param request:
    :return:
        :   -1  用户session失效  需要重新登录
        :   0   添加书签失败
        :   1   添加书签成功
    """
    user = request['session'].get('user', None)
    if user:
        bookmarkurl = request.args.get('bookmarkurl', '')
        name = request.args.get('name', '')
        chapter_url = request.args.get('chapter_url', '')
        novels_name = request.args.get('novels_name', '')
        url = bookmarkurl + "&name=" + name + "&chapter_url=" + chapter_url + "&novels_name=" + novels_name
        time = get_time()
        try:
            motor_db = MotorBase().db
            motor_db.user_message.update_one({'user': user}, {'$set': {'last_update_time': time}}, upsert=True)
            motor_db.user_message.update_one(
                {'user': user, 'bookmarks.bookmark': {'$ne': url}},
                {'$push': {'bookmarks': {'bookmark': url, 'add_time': time}}})
            LOGGER.info('书签添加成功')
            return json({'status': 1})
        except Exception as e:
            LOGGER.exception(e)
            return json({'status': 0})
    else:
        return json({'status': -1})


@operate_bp.route("/delete_bookmark", methods=['POST'])
async def owllook_delete_bookmark(request):
    """

    :param request:
    :return:
        :   -1  用户session失效  需要重新登录
        :   0   删除书签失败
        :   1   删除书签成功
    """
    user = request['session'].get('user', None)
    if user:
        bookmarkurl = request.args.get('bookmarkurl', '')
        name = request.args.get('name', '')
        chapter_url = request.args.get('chapter_url', '')
        novels_name = request.args.get('novels_name', '')
        url = bookmarkurl + "&name=" + name + "&chapter_url=" + chapter_url + "&novels_name=" + novels_name
        try:
            motor_db = MotorBase().db
            motor_db.user_message.update_one({'user': user},
                                             {'$pull': {'bookmarks': {"bookmark": url}}})
            LOGGER.info('删除书签成功')
            return json({'status': 1})
        except Exception as e:
            LOGGER.exception(e)
            return json({'status': 0})
    else:
        return json({'status': -1})


@operate_bp.route("/add_book", methods=['POST'])
async def owllook_add_book(request):
    """

    :param request:
    :return:
        :   -1  用户session失效  需要重新登录
        :   0   添加书架失败
        :   1   添加书架成功
    """
    user = request['session'].get('user', None)
    if user:
        novels_name = request.args.get('novels_name', '')
        chapter_url = request.args.get('chapter_url', '')
        url = "/chapter?url={chapter_url}&novels_name={novels_name}".format(chapter_url=chapter_url,
                                                                            novels_name=novels_name)
        time = get_time()
        try:
            motor_db = MotorBase().db
            motor_db.user_message.update_one({'user': user}, {'$set': {'last_update_time': time}}, upsert=True)
            motor_db.user_message.update_one(
                {'user': user, 'books_url.book_url': {'$ne': url}},
                {'$push': {'books_url': {'book_url': url, 'add_time': time}}})
            LOGGER.info('书架添加成功')
            return json({'status': 1})
        except Exception as e:
            LOGGER.exception(e)
            return json({'status': 0})
    else:
        return json({'status': -1})


@operate_bp.route("/delete_book", methods=['POST'])
async def owllook_delete_book(request):
    """

    :param request:
    :return:
        :   -1  用户session失效  需要重新登录
        :   0   删除书架失败
        :   1   删除书架成功
    """
    user = request['session'].get('user', None)
    if user:
        novels_name = request.args.get('novels_name', '')
        chapter_url = request.args.get('chapter_url', '')
        url = "/chapter?url={chapter_url}&novels_name={novels_name}".format(chapter_url=chapter_url,
                                                                            novels_name=novels_name)
        try:
            motor_db = MotorBase().db
            motor_db.user_message.update_one({'user': user},
                                             {'$pull': {'books_url': {"book_url": url}}})
            LOGGER.info('删除书架成功')
            return json({'status': 1})
        except Exception as e:
            LOGGER.exception(e)
            return json({'status': 0})
    else:
        return json({'status': -1})
