#!/usr/bin/env python
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.response import html, json

from novels_search.database.mongodb import MotorBase

operate_bp = Blueprint('operate_blueprint', url_prefix='operate')
operate_bp.static('/static', './static/operate')

# jinjia2 config
env = Environment(
    loader=PackageLoader('views.operate_blueprint', '../templates/operate'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


@operate_bp.route("/login")
async def index(request):
    motor_db = MotorBase().db
    doc = request
    print(doc)
    object_id = await motor_db.test.save(doc)
    return json({'object_id': str(object_id)})
