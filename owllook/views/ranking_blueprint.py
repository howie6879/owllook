#!/usr/bin/env python
from sanic import Blueprint, response
from jinja2 import Environment, PackageLoader, select_autoescape

from owllook.database.mongodb import MotorBase
from owllook.config import RULES, LOGGER, REPLACE_RULES, ENGINE_PRIORITY, BASE_DIR

rank_bp = Blueprint('ranking_blueprint', url_prefix='rank')
rank_bp.static('/static', BASE_DIR + '/static/rank')

# jinjia2 config
env = Environment(
    loader=PackageLoader('views.ranking_blueprint', '../templates/rank'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']))


@rank_bp.route("/")
async def index(request):
    motor_db = MotorBase().db
    ranking_cursor = motor_db.novels_ranking.find({})
    async for document in ranking_cursor:
        LOGGER.info(document)
    return response.text('Ranking test')
