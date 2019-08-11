#!/usr/bin/env python
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Blueprint
from sanic.exceptions import NotFound, ServerError
from sanic.response import html, json

from owllook.config import CONFIG

except_bp = Blueprint('except_blueprint', url_prefix='except')
except_bp.static('/static/except', CONFIG.BASE_DIR + '/static/except')

# jinjia2 config
env = Environment(
    loader=PackageLoader('owllook.views.except_blueprint', '../templates/except'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


def template(tpl, **kwargs):
    template = env.get_template(tpl)
    return html(template.render(kwargs))


@except_bp.exception(NotFound)
def ignore_404(request, exception):
    if "google3eabdadc11faf3b3" in request.url:
        return template('google3eabdadc11faf3b3.html')
    return template('404.html')


@except_bp.exception(ServerError)
async def server_error(request, exception):
    return json(
        {
            "exception": "{}".format(exception),
            "status": exception.status_code
        },
        status=exception.status_code)
