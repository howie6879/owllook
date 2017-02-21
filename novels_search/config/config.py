#!/usr/bin/env python
import logging
from collections import namedtuple

# Search engine
# eg:
# https://m.baidu.com/s?word=***+**
# https://www.baidu.com/s?q=&wd=python&ie=utf-8&tn=baidulocal&ct=2097152&si=jianshu.com&cl=3
# https://www.baidu.com/s?wd=%E6%8B%A9%E5%A4%A9%E8%AE%B0+%E5%B0%8F%E8%AF%B4&ie=utf-8&tn=baidulocal
# https://www.baidu.com/s?wd=python&ie=utf-8&tn=baidulocal&ct=2097152&si=cnblogs.com&rn=50
URL_PHONE = 'https://m.baidu.com/s'
URL_PC = 'http://www.baidu.com/s'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('root')

# DOMAIN
BLACK_DOMAIN = ['www.17k.com', 'mm.17k.com', 'www.xs8.cn', 'www.zongheng.com', 'yunqi.qq.com', 'chuangshi.qq.com',
                'book.qidian.com', 'www.soduso.com', 'pages.book.qq.com', 'book.km.com', 'www.lread.net',
                'www.0dsw.com', 'www.5200xsb.com', 'www.80txt.com', 'www.sodu.tw', 'www.shuquge.com',
                'www.shenmanhua.com', 'xiaoshuo.sogou.com', 'www.999wx.com', 'zetianji8.com', 'www.bookso.net',
                'm.23us.com', 'www.qbxsw.com', 'www.zhuzhudao.com', 'www.shengyan.org']

# Rules
Rules = namedtuple('Rules', 'content_url dict')
RULES = {
    # demo  'name': Rules('content_url', [selector])
    'www.biquge.com': Rules('www.biquge.com', {'class': 'box_con'}),
    'www.biqugex.com': Rules('www.biqugex.com', {'class': 'box_con'}),
    # 'www.biqule.com': Rules('www.biqule.com', {'class': 'box_con'}),
    'www.xxbiquge.com': Rules('www.xxbiquge.com', {'class': 'box_con'}),
    'www.37zw.com': Rules('www.37zw.com', {'class': 'box_con'}),
    'www.00ksw.net': Rules('www.00ksw.net', {'class': 'box_con'}),
    'www.81zw.com': Rules('www.81zw.com', {'class': 'box_con'}),
    'www.qu.la': Rules('www.qu.la', {'class': 'box_con'}),
    'www.siluke.tw': Rules('www.siluke.tw', {'class': 'box_con'}),
    'www.biquge.tw': Rules('www.biquge.tw', {'class': 'box_con'}),
    'www.shuge.net': Rules('www.shuge.net', {'class': 'box_con'}),
    'www.09xs.com': Rules('www.09xs.com', {'class': 'box_con'}),
    'www.booktxt.net': Rules('www.booktxt.net', {'class': 'box_con'}),
    'www.fs23.com': Rules('www.fs23.com', {'class': 'box_con'}),
    'www.fhxiaoshuo.com': Rules('www.fhxiaoshuo.com', {'class': 'box_con'}),
    'www.yikanxiaoshuo.com': Rules('www.yikanxiaoshuo.com', {'class': 'box_con'}),
    'www.13xs.com': Rules('www.13xs.com', {'class': 'box_con'}),
    'www.lingdiankanshu.com': Rules('www.lingdiankanshu.com', {'class': 'box_con'}),
    'www.1xiaoshuo.com': Rules('www.1xiaoshuo.com', {'class': 'box_con'}),
    'www.kanshu.la': Rules('www.kanshu.la', {'class': 'box_con'}),
    'wanmeishijiexiaoshuo.org': Rules('wanmeishijiexiaoshuo.org', {'class': 'bg'}),
    'www.jueshitangmen.info': Rules('www.jueshitangmen.info', {'class': 'bg'}),
    'zetianjiba.net': Rules('zetianjiba.net', {'class': 'bg'}),
    'www.bxwx9.org': Rules('www.bxwx9.org', {'class': 'TabCss'}),
    'www.23us.la': Rules('www.23us.la', {'class': 'inner'}),
    'www.23us.cc': Rules('www.23us.cc', {'class': 'inner'}),
    'www.sosoxiaoshuo.cc': Rules('www.sosoxiaoshuo.cc', {'class': 'box_con'}),
    'www.ciluke.com': Rules('www.ciluke.com', {'id': 'list'}),
    'www.555zw.com': Rules('www.555zw.com', {'class': 'dir'}),
    # 'www.hhlwx.com': Rules('www.hhlwx.co', {'class': 'chapterlist'}),
}
