#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from owllook.spiders.heiyan_novel_info import HYNovelInfoItem

HTML = """
<!doctype html> 
<!--[if lt IE 7]><html class="no-js ie6 oldie" lang="zh" xmlns:wb="http://open.weibo.com/wb"> <![endif]-->
<!--[if IE 7]><html class="no-js ie7 oldie" lang="zh" xmlns:wb="http://open.weibo.com/wb"> <![endif]-->
<!--[if IE 8]><html class="no-js ie8 oldie" lang="zh" xmlns:wb="http://open.weibo.com/wb"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="zh" xmlns:wb="http://open.weibo.com/wb"> <!--<![endif]--><head>
		<title>神仙微信群无广告,神仙微信群最新章节全文阅读,向阳的心的小说_黑岩网_黑岩阅读网</title>
		<meta name="keywords" content="神仙微信群，神仙微信群最新章节，神仙微信群无弹窗， 向阳的心">
		<meta name="description" content="神仙微信群是由作者（向阳的心）著作的社会题材小说，神仙微信群TXT下载,黑岩每天第一时间内更新神仙微信群最新章节,欢迎收藏。">
		<meta name="mobile-agent" content="format=xhtml;url=http://w.heiyan.com/book/62599"> 
		<meta property="og:type" content="社会"/>
		<meta property="og:title" content="神仙微信群"/>
		<meta property="og:description" content="无意间加入了神仙微信群，生活就此嗨翻天&hellip;&hellip;【黑岩第一部微信红包文，主编力荐好书】"/>
		<meta property="og:image" content="http://b.heiyanimg.com/book/62599.jpg@!bm?4"/>
		<meta property="og:url" content="http://www.heiyan.com/book/62599"/>
		<meta property="og:novel:category" content="社会"/>
		<meta property="og:novel:author" content=" 向阳的心"/>
		<meta property="og:novel:book_name" content="神仙微信群"/>
		<meta property="og:novel:status" content="连载中"/>
		<meta property="og:novel:read_url" content="http://www.heiyan.com/book/62599"/>
		<meta property="og:novel:update_time" content="昨天22:52"/>
		<meta property="og:novel:latest_chapter_name" content="2362 禁忌之恋"/>
		<meta property="og:novel:latest_chapter_url" content="http://www.heiyan.com/book/62599/2424103"/>
		<link rel="stylesheet" type="text/css" href="http://st.heiyanimg.com/_static/components/jqueryui/themes/ui-lightness/jquery-ui.min.css" media="all" />
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="Cache-Control" content="no-transform" />

"""


def test_heiyan_novel_info():
    url = 'http://www.heiyan.com/book/62599'
    item_data = HYNovelInfoItem.get_item(html=HTML)

    assert item_data['novel_name'] == '神仙微信群'
