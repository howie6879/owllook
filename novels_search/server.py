#!/usr/bin/env python
from sanic import Sanic
from novels_search.views.novels_blueprint import novels_bp
from novels_search.views.operate_blueprint import operate_bp

app = Sanic(__name__)
app.blueprint(novels_bp)
app.blueprint(operate_bp)
app.run(host="0.0.0.0", port=8000, debug=True)
