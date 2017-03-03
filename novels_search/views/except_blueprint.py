#!/usr/bin/env python
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError
from sanic.response import html, json
from jinja2 import Environment, PackageLoader, select_autoescape

except_bp = Blueprint('except_blueprint', url_prefix='except')
except_bp.static('/static', './static/except')

# jinjia2 config
env = Environment(
    loader=PackageLoader('views.except_blueprint', '../templates/except'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


@except_bp.exception(NotFound)
def ignore_404s(request, exception):
    return template('404.html')


@except_bp.exception(ServerError)
async def test(request, exception):
    return json(
        {
            "exception": "{}".format(exception),
            "status": exception.status_code
        },
        status=exception.status_code)
