#!/usr/bin/env python
import uvloop
import asyncio
import time
from pprint import pprint
from novels_search.fetcher.baidu_novels import baidu_search as search

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def novel_task(name, is_web=1):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(search(name, is_web))
    loop.run_until_complete(task)
    return task.result()


start = time.time()
result = novel_task('择天记 阅读 小说', 1)
pprint(result)
print(time.time() - start)


# output

# [{'is_parse': 1,
#       'netloc': 'www.00ksw.net',
#       'time': '',
#       'timestamp': 0,
#       'title': '择天记_择天记最新章节_择天记全文阅读_猫腻_零点看书',
#       'url': 'http://www.00ksw.net/html/13/13835/'},
#      {'is_parse': 1,
#       'netloc': 'www.23us.com',
#       'time': '',
#       'timestamp': 0,
#       'title': '择天记 最新章节 无弹窗广告 - 顶点小说',
#       'url': 'http://www.23us.com/html/52/52234/'},
#      {'is_parse': 1,
#       'netloc': 'www.kanshu.la',
#       'time': '',
#       'timestamp': 0,
#       'title': '择天记最新章节列表,择天记5200,全文阅读-看书啦小说网',
#       'url': 'http://www.kanshu.la/book/zetianji/'},
#      {'is_parse': 1,
#       'netloc': 'www.booktxt.net',
#       'time': '',
#       'timestamp': 0,
#       'title': '择天记最新章节_择天记无弹窗全文阅读_顶点小说',
#       'url': 'http://www.booktxt.net/0_67/'},
#      {'is_parse': 1,
#       'netloc': 'www.81zw.com',
#       'time': '',
#       'timestamp': 0,
#       'title': '择天记最新章节,择天记无弹窗全文阅读 - 八一中文网',
#       'url': 'http://www.81zw.com/book/8634/'},
#      {'is_parse': 1,
#       'netloc': 'www.xxbiquge.com',
#       'time': '',
#       'timestamp': 0,
#       'title': '择天记最新章节列表_择天记最新章节目录_新笔趣阁',
#       'url': 'http://www.xxbiquge.com/5_5422/'},
#      {'is_parse': 0,
#       'netloc': 'www.kanshula.org',
#       'time': '',
#       'timestamp': 0,
#       'title': '择天记最新章节_猫腻_择天记全文阅读_看书啦',
#       'url': 'http://www.kanshula.org/8_8333/0.html'}, ]
