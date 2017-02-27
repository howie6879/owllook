#!/usr/bin/env python
from sanic import Sanic
import sys
sys.path.append('/Users/howie/Documents/programming/python/git/novels-search')
from novels_search.novels_blueprint import bp

app = Sanic(__name__)
app.blueprint(bp)

app.run(host="0.0.0.0", port=8000, debug=True)
