#!/usr/bin/env python
import hashlib
import arrow

from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.response import html, json

from novels_search.database.mongodb import MotorBase
from novels_search.config import WEBSITE, TIMEZONE

operate_bp = Blueprint('operate_blueprint', url_prefix='operate')
operate_bp.static('/static', './static/operate')

# jinjia2 config
env = Environment(
    loader=PackageLoader('views.operate_blueprint', '../templates/operate'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


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
            utc = arrow.utcnow()
            local = utc.to(TIMEZONE)
            time = local.format("YYYY-MM-DD HH:mm:ss")
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

