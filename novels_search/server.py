#!/usr/bin/env python
import aiocache
from sanic import Sanic
from sanic.response import html
from sanic_session import RedisSessionInterface

from novels_search.views.novels_blueprint import novels_bp
from novels_search.views.operate_blueprint import operate_bp
from novels_search.views.except_blueprint import except_bp
from novels_search.views.admin_blueprint import admin_bp
from novels_search.database.redis import RedisSession
from novels_search.config import WEBSITE, REDIS_DICT

app = Sanic(__name__)
app.blueprint(novels_bp)
app.blueprint(operate_bp)
app.blueprint(except_bp)
app.blueprint(admin_bp)


@app.listener('before_server_start')
def init_cache(sanic, loop):
    aiocache.settings.set_defaults(
        class_="aiocache.RedisCache",
        endpoint=REDIS_DICT.get('REDIS_ENDPOINT', None),
        port=REDIS_DICT.get('REDIS_PORT', None),
        db=REDIS_DICT.get('CACHE_DB', None),
        password=REDIS_DICT.get('PASSWORD', None),
        loop=loop,
    )


redis = RedisSession()

# pass the getter method for the connection pool into the session
session_interface = RedisSessionInterface(redis.get_redis_pool, expiry=604800)


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    if WEBSITE['IS_RUNNING']:
        await session_interface.open(request)
    else:
        return html("<h3>网站正在维护...</h3>")


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    if request.get('session', None):
        await session_interface.save(request, response)


app.run(host="0.0.0.0", workers=1, port=8000, debug=True)
