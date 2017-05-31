#!/usr/bin/env python
import aiocache
from sanic import Sanic
from sanic.response import html, redirect
from sanic_session import RedisSessionInterface

import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from owllook.views.novels_blueprint import novels_bp
from owllook.views.operate_blueprint import operate_bp
from owllook.views.except_blueprint import except_bp
from owllook.views.admin_blueprint import admin_bp
from owllook.views.api_blueprint import api_bp
from owllook.database.redis import RedisSession
from owllook.config import WEBSITE, REDIS_DICT, LOGGER, HOST

app = Sanic(__name__)
app.blueprint(novels_bp)
app.blueprint(operate_bp)
app.blueprint(except_bp)
app.blueprint(admin_bp)
app.blueprint(api_bp)


@app.listener('before_server_start')
def init_cache(sanic, loop):
    LOGGER.info("Starting aiocache")
    aiocache.settings.set_defaults(
        class_="aiocache.RedisCache",
        endpoint=REDIS_DICT.get('REDIS_ENDPOINT', None),
        port=REDIS_DICT.get('REDIS_PORT', None),
        db=REDIS_DICT.get('CACHE_DB', None),
        password=REDIS_DICT.get('PASSWORD', None),
        loop=loop,
    )
    LOGGER.info("Starting redis pool")
    redis = RedisSession()
    # redis instance for app
    app.get_redis_pool = redis.get_redis_pool
    # pass the getter method for the connection pool into the session
    app.session_interface = RedisSessionInterface(app.get_redis_pool, cookie_name="owl_sid", expiry=30 * 24 * 60 * 60)


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    host = request.headers.get('host', None)
    if not host or host not in HOST:
        return redirect('http://www.owllook.net')
    if WEBSITE['IS_RUNNING']:
        await app.session_interface.open(request)
    else:
        return html("<h3>网站正在维护...</h3>")


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    # await app.session_interface.save(request, response)
    if request.path == '/operate/login' and request['session'].get('user', None):
        await app.session_interface.save(request, response)
        import datetime
        response.cookies['owl_sid']['expires'] = datetime.datetime.now() + datetime.timedelta(days=30)
    elif request.path == '/register':
        try:
            response.cookies['reg_index'] = str(request['session']['index'][0])
        except KeyError:
            pass


if __name__ == "__main__":
        app.run(host="127.0.0.1", workers=1, port=8001, debug=True)
