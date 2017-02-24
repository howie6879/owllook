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
BAIDU_RN = 50
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('root')

# DOMAIN
BLACK_DOMAIN = ['www.17k.com', 'mm.17k.com', 'www.xs8.cn', 'www.zongheng.com', 'yunqi.qq.com', 'chuangshi.qq.com',
                'book.qidian.com', 'www.soduso.com', 'pages.book.qq.com', 'book.km.com', 'www.lread.net',
                'www.0dsw.com', 'www.5200xsb.com', 'www.80txt.com', 'www.sodu.tw', 'www.shuquge.com',
                'www.shenmanhua.com', 'xiaoshuo.sogou.com', 'www.999wx.com', 'zetianji8.com', 'www.bookso.net',
                'm.23us.com', 'www.qbxsw.com', 'www.zhuzhudao.com', 'www.shengyan.org', 'www.360doc.com',
                'www.ishuo.cn', 'read.qidian.com', 'www.yunlaige.com', 'www.qidian.com', 'www.sodu888.com']

# Rules
Rules = namedtuple('Rules', 'content_url chapter_selector content_selector')
RULES = {
    # demo  'name': Rules('content_url', {chapter_selector}, {content_selector})
    # 已解析
    'www.biquge.com': Rules('www.biquge.com', {'class': 'box_con'}, {}),
    # 已解析
    'www.biqugex.com': Rules('0', {'class': 'box_con'}, {}),
    # 'www.biqule.com': Rules('www.biqule.com', {'class': 'box_con'},{}),
    'www.qu.la': Rules('www.qu.la', {'class': 'box_con'}, {}),
    'www.siluke.tw': Rules('www.siluke.tw', {'class': 'box_con'}, {}),
    'www.shuge.net': Rules('www.shuge.net', {'class': 'box_con'}, {}),
    'www.09xs.com': Rules('www.09xs.com', {'class': 'box_con'}, {}),
    'www.fhxiaoshuo.com': Rules('www.fhxiaoshuo.com', {'class': 'box_con'}, {}),
    'www.yikanxiaoshuo.com': Rules('www.yikanxiaoshuo.com', {'class': 'box_con'}, {}),
    'www.lingdiankanshu.com': Rules('www.lingdiankanshu.com', {'class': 'box_con'}, {}),
    'www.1xiaoshuo.com': Rules('www.1xiaoshuo.com', {'class': 'box_con'}, {}),
    'www.kanshu.la': Rules('www.kanshu.la', {'class': 'box_con'}, {}),
    'www.bxwx.org': Rules('0', {'class': 'TabCss'}, {}),
    # 'www.hhlwx.com': Rules('www.hhlwx.co', {'class': 'chapterlist'},{}),
    # 已解析
    'www.lingyu.org': Rules('http://www.lingyu.org', {'class': 'mt10'}, {}),
    'www.kbiquge.com': Rules('http://www.kbiquge.com', {'class': 'box_con'}, {}),

    # 已解析
    'www.00ksw.net': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.booktxt.net': Rules('http://www.booktxt.net', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析  content_url=1表示章节链接使用本身自带的链接，不用拼接
    'wanmeishijiexiaoshuo.org': Rules('1', {'class': 'bg'}, {'class': 'content'}),
    # 已解析
    'www.sosoxiaoshuo.cc': Rules('http://www.sosoxiaoshuo.cc', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.ciluke.com': Rules('0', {'id': 'list'}, {'id': 'content'}),
    # 已解析
    'www.81zw.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.cilook.net': Rules('0', {'id': 'cl_content'}, {'id': 'content'}),
    # 已解析  content_url=1表示章节链接使用本身自带的链接，不用拼接
    'www.baoliny.com': Rules('1', {'class': 'readerListShow'}, {'id': 'content'}),
    # 已解析
    'www.biquge.tw': Rules('http://www.biquge.tw', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.is028.cn': Rules('http://www.biquge.com.tw', {'class': 'box_con'}, {'id': 'content'}),
    # www.is028.cn会跳转到http://www.biquge.com.tw
    'www.biquge.com.tw': Rules('http://www.biquge.com.tw', {'class': 'box_con'}, {'id': 'content'}),
    # 'www.xs82.com': Rules('-1', {'class': 'chapterlist'}, {'id': 'content'}),
    # 已解析
    'www.shuqizw.com': Rules('http://www.shuqizw.com', {'class': 'article_texttitleb'}, {'id': 'book_text'}),
    # 已解析
    'read.ixdzs.com': Rules('0', {'class': 'catalog'}, {'class': 'content'}),
    # 已解析
    'www.shumilou.net': Rules('0', {'class': 'chapterlist'}, {'id': 'BookText'}),
    # 已解析
    # 'www.ttshu.com': Rules('http://www.ttshu.com', {'class': 'border'}, {'id': 'content'}),
    # 已解析
    'www.heiyan.la': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.bbsa5.com': Rules('1', {'class': 'panel'}, {'class': 'content-body'}),
    # 已解析
    'www.tycqxs.com': Rules('http://www.tycqxs.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.miaobige.com': Rules('0', {'id': 'readerlists'}, {'id': 'content'}),
    # 已解析
    'www.dashubao.net': Rules('0', {'class': 'ml_main'}, {'class': 'yd_text2'}),
    # 已解析 content_url=0表示章节网页需要当前页面url拼接
    'www.23zw.com': Rules('0', {'id': 'chapter_list'}, {'id': 'text_area'}),
    # 已解析
    'www.23us.la': Rules('http://www.23us.la', {'class': 'inner'}, {'id': 'content'}),
    # 已解析
    'www.23us.cc': Rules('0', {'class': 'inner'}, {'id': 'content'}),
    # 已解析
    'www.13xs.com': Rules('0', {'class': 'box_con'}, {'id': 'booktext'}),
    # 已解析
    'www.tsxsw.com': Rules('0', {'class': 'bdsub'}, {'id': 'contents'}),
    # 已解析
    'zetianjiba.net': Rules('1', {'class': 'bg'}, {'class': 'content'}),
    # 已解析
    'www.37zw.com': Rules('0', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.555zw.com': Rules('0', {'class': 'dir'}, {'id': 'content'}),
    # 已解析  content_url=1表示章节链接使用本身自带的链接，不用拼接
    'www.jueshitangmen.info': Rules('1', {'class': 'bg'}, {'class': 'content'}),
    # 已解析 content_url=0表示章节网页需要当前页面url拼接
    'www.bxwx9.org': Rules('0', {'class': 'TabCss'}, {'id': 'content'}),
    # 已解析
    'www.xxbiquge.com': Rules('http://www.xxbiquge.com', {'class': 'box_con'}, {'id': 'content'}),
    # 已解析
    'www.fs23.com': Rules('http://www.fs23.com', {'class': 'box_con'}, {'id': 'content'}),

}
