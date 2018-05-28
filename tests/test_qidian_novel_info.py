#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""

import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from owllook.spiders.qidian_novel_info import QidianNovelInfoItem

HTML = """

<!DOCTYPE html>
<html>
<head>
    
    <meta charset="UTF-8">
    <title>《圣墟》_辰东著_玄幻_起点中文网</title>
    <meta name="description" content="圣墟，圣墟小说阅读。玄幻小说圣墟由作家辰东创作，起点小说提供圣墟首发最新章节及章节列表，圣墟最新更新尽在起点中文网">
    <meta name="keywords" content="圣墟,楚风,场域,席勒,异人,兽王,大黑牛,王级强者,挣断,玉虚宫,陆通">
    <meta name="robots" content="all">
    <meta name="googlebot" content="all">
    <meta name="baiduspider" content="all">
    <meta http-equiv="mobile-agent" content="format=wml; url=http://m.qidian.com/book/showbook.aspx?bookid=1004608738">
    <meta http-equiv="mobile-agent" content="format=xhtml; url=http://m.qidian.com/book/showbook.aspx?bookid=1004608738">
    <meta http-equiv="mobile-agent" content="format=html5; url=http://m.qidian.com/book/showbook.aspx?bookid=1004608738">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">
    <meta name="renderer" content="webkit" />
    <script>
        document.domain = 'qidian.com';
    </script>
    <script>
        var speedTimer = [],
        speedZero = new Date().getTime();
    </script>
    <script>
        function getCookie(name) {
            var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
            arr = document.cookie.match(reg);
            if (arr){
                return arr[2];
            }else {
                return null;
            }
        }
        // tf = 1 用户选择，留在PC
        if (getCookie('tf') != 1) {
            if(/Android|Windows Phone|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)){
                window.location.href="//m.qidian.com/book/1004608738";
            }
        }else{
            // M站设置了一年，这里fixed
            setCookie('tf', 1, 'qidian.com', '/', 0);
        }
    </script>
    
<script>
    //遇到cookie tf=1的话留在本站，否则跳转移动站
    if (getCookie('tf') != 1) {
        //判断是以下设备后跳转到m站
        if (navigator.userAgent.match(/(iPhone|iPod|Android)/i)) {
            location.href = "//m.qidian.com"
        }
    }else {
        // M站设置了一年，这里fixed
        setCookie('tf', 1, 'qidian.com', '/', 0);
    }
    // start 防劫持
    //设置cookie
    function setCookie(name, value, domain, path, expires) {
        if(expires){
            expires = new Date(+new Date() + expires);
        }
        var tempcookie = name + '=' + escape(value) +
                ((expires) ? '; expires=' + expires.toGMTString() : '') +
                ((path) ? '; path=' + path : '') +
                ((domain) ? '; domain=' + domain : '');
        //Ensure the cookie's size is under the limitation
        if(tempcookie.length < 4096) {
            document.cookie = tempcookie;
        }
    }
    //获取cookie
    function getCookie(name) {
        var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
        if (arr = document.cookie.match(reg))
            return (arr[2]);
        else
            return null;
    }
    //创建并发送请求
    function createSender(url){
        var img = new Image();
        img.onload = img.onerror = function(){
            img = null;
        };
        img.src = url;
    };
</script>

<link data-ignore="true" rel="shortcut icon" type="image/x-icon" href="//qidian.gtimg.com/qd/favicon/qd_icon.c443c.ico">
<link data-ignore="true" rel="Bookmark" type="image/x-icon" href="//qidian.gtimg.com/qd/favicon/qd_icon.c443c.ico">


    
<link rel="stylesheet" data-ignore="true" href="//qidian.gtimg.com/c/=/qd/css/lbfUI/css/icon.a578d.css,/qd/css/lbfUI/css/Drag.41d31.css,/qd/css/reset.ddecf.css,/qd/css/global.d41d8.css,/qd/css/font.089a4.css,/qd/css/footer.feb73.css,/qd/css/qd_popup.7e65f.css,/qd/css/book_popup.18f47.css,/qd/css/vote_popup.3844d.css,/qd/icon/forum/sprite.445f4.css,/qd/css/forum/emoji.c4e81.css" />

    
    <link data-ignore="true" rel="stylesheet" href="//qidian.gtimg.com/qd/css/module.429f5.css">
    <link data-ignore="true" rel="stylesheet" href="//qidian.gtimg.com/qd/css/layout.5de0f.css">
    <link data-ignore="true" rel="stylesheet" href="//qidian.gtimg.com/qd/css/book_details.1ccd3.css">
    
</head>
<body>
<div class="share-img">
    <img src="//qidian.gtimg.com/qd/images/common/share.6aa92.png" width='300' height="300">
</div>

<div class="wrap">
    
    
    
<div id="pin-nav" class="pin-nav-wrap need-search" data-l1="40">
    <div class="box-center cf">
        <div class="nav-list site-nav fl">
            <ul>
                <li class="site"><a class="pin-logo" href="//www.qidian.com" data-eid="qd_A43"><span></span></a>
                    <div class="dropdown">
                        <a href="https://www.qdmm.com" target="" data-eid="qd_A44">起点女生网</a>
                        <a href="http://chuangshi.qq.com" target="" data-eid="qd_A45">创世中文网</a>
                        <a href="http://yunqi.qq.com" target="" data-eid="qd_A46">云起书院</a>
                    </div>
                </li>
                <li><a href="//www.qidian.com/xuanhuan" target="" data-eid="qd_A47">玄幻</a></li>
                <li><a href="//www.qidian.com/dushi" target="" data-eid="qd_A48">都市</a></li>
                <li><a href="//www.qidian.com/xianxia" target="" data-eid="qd_A49">仙侠</a></li>
                <li><a href="//www.qidian.com/kehuan" target="" data-eid="qd_A50">科幻</a></li>
                <li><a href="//www.qidian.com/youxi" target="" data-eid="qd_A56">游戏</a></li>
                <li><a href="//www.qidian.com/lishi" target="" data-eid="qd_A52">历史</a></li>
                <li><a href="//www.qidian.com/rank" target="_blank" data-eid="qd_A53">排行</a></li>
                <li class="more"><a href="javascript:" id="top-nav-more" target="" data-eid="qd_A54">更多<span></span></a>
                    <div class="dropdown">
                        <a href="//www.qidian.com/all" target="_blank" data-eid="qd_A169">全部作品</a>
                        <a href="//www.qidian.com/2cy" target="" data-eid="qd_A55">二次元</a>
                        <a href="//www.qidian.com/qihuan" target="" data-eid="qd_A51">奇幻</a>
                        <a href="//www.qidian.com/wuxia" target="" data-eid="qd_A57">武侠</a>
                        <a href="//www.qidian.com/lingyi" target="" data-eid="qd_A58">灵异</a>
                        <a href="//www.qidian.com/junshi" target="" data-eid="qd_A59">军事</a>
                        <a href="//www.qidian.com/xianshi" target="" data-eid="qd_A60">现实</a>
                        <a href="//www.qidian.com/tiyu" target="" data-eid="qd_A61">体育</a>
                        <a href="//www.qidian.com/duanpian" target="" data-eid="qd_A196">短篇</a>
                    </div>
                </li>
            </ul>
        </div>
        <div class="nav-list min-user fr">
            <ul>
                <li id="min-search">
                    <form id="formUrl" action="//www.qidian.com/search" method="get" target="_blank">
                        <label id="pin-search" for="topSearchSubmit" data-eid="qd_A62"><em class="iconfont">&#xe60d;</em>
                        </label>
                        <input id="pin-input" class="pin-input hide" type="text" name="kw" placeholder="读书成圣">
                        <input class="submit-input" type="submit" id="topSearchSubmit" data-eid="qd_A62">
                    </form>
                </li>
                <li class="line"></li>
                <li class="sign-out">
                    <a id="pin-login" href="javascript:" data-eid="qd_A64">登录</a>
                    <a class="reg" href="//passport.qidian.com/reg.html?appid=10&areaid=1&target=iframe&ticket=1&auto=1&autotime=30&returnUrl=https%3A%2F%2Fwww.qidian.com" target="_blank">注册</a>
                </li>
                <li class="sign-in hidden">
                    <a href="//me.qidian.com/Index.aspx" target="_blank" data-eid="qd_A65"><i id="nav-user-name"></i><span></span></a>
                    <div class="dropdown">
                        <a href="//me.qidian.com/msg/lists.aspx?page=1" target="_blank" data-eid="qd_A66">消息(<i id="top-msg">0</i>)</a>
                        <a href="//www.qidian.com/charge/meRedirect" target="_blank" data-eid="qd_A67">充值</a>
                        <a href="//me.qidian.com/Index.aspx" target="_blank" data-eid="qd_A68">个人中心</a>
                        <a href="//www.qidian.com/help/kf" target="_blank" data-eid="qd_A69">客服中心</a>
                        <a id="exit" href="javascript:" data-eid="qd_A70">退出</a>
                    </div>
                </li>
                <li class="line"></li>
                <li class="book-shelf" id="top-book-shelf">
                    <a href="//me.qidian.com/bookCase/bookCase.aspx" target="_blank" data-eid="qd_A63"><em class="iconfont">&#xe60c;</em><i>我的书架
                    </i></a></li>
            </ul>
        </div>
    </div>
</div>

    
    

<div id="j-topHeadBox" class="top-bg-op-box " data-cookie="1" style="background-image:url('//qidian.qpic.cn/qidian_common/349573/fa2bbd54ddab669f289f138f15730f01/0')" data-l1="1">
    <a class="jumpWrap" href="http://cpgame.qd.game.qidian.com/Home/Index/directLogin/name/jsxw/way/1?qd_game_key=jsxw2560x450&amp;qd_dd_p1=658" target="_blank" data-eid="qd_G100" data-qd_dd_p1="1">
        <span class="op-tag"></span>
    </a>
    <a class="close-game-op" id="closeTopGame" href="javascript:" data-eid="qd_G101">关闭广告</a>
    
</div>
<div class="top-bg-box " id="j-topBgBox" style="background-image:url('//qidian.qpic.cn/qidian_common/349573/7f689b6db8ad99e6093bae7db9a7d130/0')">
    <span class="back-to-op" data-eid="qd_G106">热门游戏</span>
</div>

<div class="crumbs-nav center990  top-op" data-l1="1">
    
    <span>
        <cite class="lt"></cite>
        
    <a href="//www.qidian.com" data-eid="qd_G01">首页</a><em class="iconfont">&#xe621;</em>
    
        <a href="//xuanhuan.qidian.com" target="_blank" data-eid="qd_G02">玄幻频道</a><em class="iconfont">&#xe621;</em>
        
        <a href="//www.qidian.com/all?chanId=21&subCateId=8" target="_blank">东方玄幻</a><em class="iconfont">&#xe621;</em>
        
    
    <a href="//book.qidian.com/info/1004608738">圣墟</a>
        <cite class="rt"></cite>
    </span>
</div>
<div class="border-shadow ">
    <span></span>
    <span></span>
</div>

    <div class="book-detail-wrap center990">
        <div class="book-information cf" data-l1="2">

    
    <div class="book-img">
        <a class="J-getJumpUrl" id="bookImg" href="//read.qidian.com/chapter/_AaqI-dPJJ4uTkiRw_sFYA2/eSlFKP1Chzg1" data-eid="qd_G09" data-bid="1004608738" data-firstchapterjumpurl="//read.qidian.com/chapter/_AaqI-dPJJ4uTkiRw_sFYA2/eSlFKP1Chzg1"><img src="//qidian.qpic.cn/qdbimg/349573/1004608738/180
"></a>
    </div>
    
    <div class="book-info ">
        <h1>
            
            <em>圣墟</em>
            <span><a class="writer" href="//me.qidian.com/authorIndex.aspx?id=4362453" target="_blank" data-eid="qd_G08">辰东</a> 著</span>
            
        </h1>
        <p class="tag"><span class="blue">连载</span>
            
            <span class="blue">签约</span>
            
            
            <span class="blue">VIP</span>
            
            <a href="//xuanhuan.qidian.com" class="red" target="_blank" data-eid="qd_G10">玄幻</a>
            
            <a href="//www.qidian.com/all?chanId=21&subCateId=8" class="red" target="_blank" data-eid="qd_G11">东方玄幻</a>
            
            
        </p>
        
        <p class="intro">在破败中崛起，在寂灭中复苏。沧海成尘，雷电枯竭……  </p>
        <p><em><style>@font-face { font-family: btVAXwWx; src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.eot?') format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.woff') format('woff'), url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.ttf') format('truetype'); } .btVAXwWx { font-family: 'btVAXwWx' !important;     display: initial !important; color: inherit !important; vertical-align: initial !important; }</style><span class="btVAXwWx">&#100405;&#100408;&#100407;&#100401;&#100407;&#100409;</span></em><cite>万字</cite><i>|</i><em><style>@font-face { font-family: btVAXwWx; src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.eot?') format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.woff') format('woff'), url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.ttf') format('truetype'); } .btVAXwWx { font-family: 'btVAXwWx' !important;     display: initial !important; color: inherit !important; vertical-align: initial !important; }</style><span class="btVAXwWx">&#100405;&#100409;&#100410;&#100405;&#100401;&#100408;&#100408;</span></em><cite>万总点击<span>&#183;</span>会员周点击<style>@font-face { font-family: btVAXwWx; src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.eot?') format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.woff') format('woff'), url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.ttf') format('truetype'); } .btVAXwWx { font-family: 'btVAXwWx' !important;     display: initial !important; color: inherit !important; vertical-align: initial !important; }</style><span class="btVAXwWx">&#100409;&#100407;&#100401;&#100407;&#100403;</span>万</cite><i>|</i><em><style>@font-face { font-family: btVAXwWx; src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.eot?') format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.woff') format('woff'), url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.ttf') format('truetype'); } .btVAXwWx { font-family: 'btVAXwWx' !important;     display: initial !important; color: inherit !important; vertical-align: initial !important; }</style><span class="btVAXwWx">&#100406;&#100406;&#100405;&#100399;&#100401;&#100403;&#100402;</span></em><cite>万总推荐<span>&#183;</span>周<style>@font-face { font-family: btVAXwWx; src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.eot?') format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.woff') format('woff'), url('https://qidian.gtimg.com/qd_anti_spider/btVAXwWx.ttf') format('truetype'); } .btVAXwWx { font-family: 'btVAXwWx' !important;     display: initial !important; color: inherit !important; vertical-align: initial !important; }</style><span class="btVAXwWx">&#100409;&#100401;&#100410;&#100407;</span>万</cite></p>
        
        <p><a class="red-btn J-getJumpUrl " href="//read.qidian.com/chapter/_AaqI-dPJJ4uTkiRw_sFYA2/eSlFKP1Chzg1" id="readBtn" data-eid="qd_G03" data-bid="1004608738" data-firstchapterjumpurl="//read.qidian.com/chapter/_AaqI-dPJJ4uTkiRw_sFYA2/eSlFKP1Chzg1">免费试读</a><a class="blue-btn add-book" id="addBookBtn" href="javascript:" data-eid="qd_G05" data-bookId="1004608738" data-bid="1004608738">加入书架</a>
            
            <a class="blue-btn" id="topVoteBtn" href="javascript:" data-showtype="1" data-eid="qd_G06">投票互动</a>
            
        </p>
        
    </div>
    
    <div class="comment-wrap">
        <div id="commentWrap">
            <div class="load-score">
                <div class="la-ball-pulse">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            <div class="j_getData hidden">
                <h4 id="j_bookScore"><span><cite id="score1">0</cite><em>.</em></span><i id="score2">0</i></h4>
                <p id="j_userCount"><span></span>人评价</p>
            </div>
        </div>
        <h5>我要评价</h5>
        <div class="score-mid" id="scoreBtn" data-score="" data-comment="0" data-eid="qd_G12">
            
            <img src="//qidian.gtimg.com/qd/images/book_details/star-off.b2a1b.png">
            
            <img src="//qidian.gtimg.com/qd/images/book_details/star-off.b2a1b.png">
            
            <img src="//qidian.gtimg.com/qd/images/book_details/star-off.b2a1b.png">
            
            <img src="//qidian.gtimg.com/qd/images/book_details/star-off.b2a1b.png">
            
            <img src="//qidian.gtimg.com/qd/images/book_details/star-off.b2a1b.png">
            
        </div>
    </div>
    <div class="take-wrap">
        
        <a class="blue" target="_blank" href="//www.webnovel.com/book/6831980302001405" data-eid="qd_G115"><em class="iconfont">&#xe67d;</em>海外同步</a>
        
        <i></i>
        
        
        
            <a class="blue" id="subscribe" href="javascript:" data-eid="qd_G13"><em class="iconfont">&#xe636;</em>订阅</a>
        
        
        <i></i>
        
        
        <a class="blue download" id="download" href="javascript:" data-eid="qd_G14"><em class="iconfont">&#xe644;</em>下载
        
    </a>
    </div>
    

</div>

        
        <div class="content-nav-wrap cf" data-l1="3">
            <div class="nav-wrap fl">
                <ul>
                    <li class="act"><a class="lang" id="j-bookInfoPage" href="javascript:" data-eid="qd_G15">作品信息</a></li>
                    <li class="j_catalog_block"><a class="lang" href="javascript:" id="j_catalogPage" data-eid="qd_G16">目录<i><span id="J-catalogCount"></span></i></a></li>
                    
                    <li class="j_discussion_block"><a class="lang" href="//forum.qidian.com/NewForum/List.aspx?BookId=1004608738" target="_blank" data-eid="qd_G17">作品讨论<i><span id="J-discusCount"></span></i></a></li>
                    
                </ul>
            </div>
        </div>
        <div class="catalog-content-wrap hidden" id="j-catalogWrap" data-l1="14">
            <div class="go-top">
                <div class="go-top-wrap">
                    <a href="#" class="icon-go-top"><em class="iconfont" data-eid="qd_G72">&#xe66b;</em></a>
                </div>
            </div>
            
            <div class="loading">
                <div class="la-ball-pulse">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            
        </div>
        
        <div class="book-content-wrap cf">
            
            <div class="left-wrap fl">
                <div class="book-info-detail">
                    <cite class="icon-pin"></cite>
                    <div class="book-intro">
                        <p>
                            
                                　　在破败中崛起，在寂灭中复苏。<br>　　沧海成尘，雷电枯竭，那一缕幽雾又一次临近大地，世间的枷锁被打开了，一个全新的世界就此揭开神秘的一角……
                            
                        </p>
                    </div>
                    <div class="book-state" data-l1="4">
                        <ul>
                            
                            
                            
                                
                                <li class="honor" id="honor">
                                    <b>荣誉动态</b>
                                    <div class="detail">
                                    <strong>2018-05-01 获得了男频月票榜(2018年04月)第三名<em class="iconfont">&#xe623;</em></strong>
                                    
                                    <div class="more-honor-wrap" id="moreHonorWrap">
                                        <cite><em></em></cite>
                                        <dl>
                                            
                                            <dd>2018-04-01 获得了男频月票榜(2018年03月)第三名</dd>
                                            
                                            <dd>2018-03-01 获得了男频月票榜(2018年02月)第三名</dd>
                                            
                                            <dd>2018-02-01 获得了男频月票榜(2018年01月)第三名</dd>
                                            
                                            <dd>2018-01-01 获得了男频月票榜(2017年12月)第三名</dd>
                                            
                                            <dd>2017-12-01 获得了男频月票榜(2017年11月)第二名</dd>
                                            
                                            <dd>2017-11-01 获得了男频月票榜(2017年10月)第一名</dd>
                                            
                                            <dd>2017-10-01 获得了男频月票榜(2017年09月)第一名</dd>
                                            
                                            <dd>2017-09-01 获得了男频月票榜(2017年08月)第一名</dd>
                                            
                                            <dd>2017-07-31 获得了月票榜(2017年07月)第一名</dd>
                                            
                                        </dl>
                                    </div>
                                    
                                    <p class="honor-icon cf">
                                        
                                        <img src="//qidian.gtimg.com/qd/images/book/badges/wanzhongyixin.png">
                                        
                                        <img src="//qidian.gtimg.com/qd/images/book/badges/yuepiaodiyi.png">
                                        
                                        <img src="//qidian.gtimg.com/qd/images/book/badges/baimengzhengba.png">
                                        
                                        <img src="//qidian.gtimg.com/qd/images/book/badges/gengshangyicenglou.png">
                                        
                                        <a class="blue collect" href="//book.qidian.com/honor/1004608738" target="_blank" data-eid="qd_G18">荣誉殿堂</a>
                                    </p>
                                    </div>
                                </li>
                                
                            
                                <li class="update">
                                    <b>最近更新</b>
                                    <div class="detail">
                                        <p class="cf">
                                            <a class="blue" href="//vipreader.qidian.com/chapter/1004608738/409872731" data-eid="qd_G19" data-cid="//vipreader.qidian.com/chapter/1004608738/409872731" title="第1070章 千古有缘再相会" target="_blank">第1070章 千古有缘再相会</a><i>&#183;</i><em class="time">9小时前</em>
                                        </p>
                                        <p class="tag-wrap mt10">
                                            
                                            
                                            <span class="tags red">连续13天更新</span>
                                            
                                        </p>
                                    </div>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="fans-zone" data-l1="5">
                    <h3 class="lang">粉丝互动</h3>
                    <div class="fans-interact cf">
                        <dl>
                            <dd>
                                <h4 id="ticket-Tab">
                                    
                                    <a class="lang act" href="javascript:" data-eid="qd_G20">月票</a><em>|</em>
                                    
                                    <a class="lang " href="javascript:" data-eid="qd_G21">推荐票
                                    
                                    </a>
                                </h4>
                                <div class="action-wrap" id="ticket-wrap">
                                    
                                    <div class="ticket month-ticket">
                                        <p>本月票数</p>
                                        <p class="num"><i id="monthCount">46548</i></p>
                                        
                                        <p>排名5<i>&#183;</i>还差<em>
                                    4306
                                    
                                     </em>票就被后一名追上</p>
                                        
                                        <div class="icon-box month">
                                            <span></span>
                                            <b></b>
                                        </div>
                                        <a class="red-radius-btn" id="monthBtn" href="javascript:" data-showtype="1" data-eid="qd_G22"><em class="iconfont">&#xe63f;</em>投月票</a>
                                        <p class="tip"><cite>1</cite>张月票=<cite>100</cite>点粉丝值</p>
                                    </div>
                                    
                                    <div class="ticket rec-ticket hidden">
                                        <p>本周票数</p>
                                        <p class="num"><i id="recCount">20147</i></p>
                                        
                                        <p>排名6<i>&#183;</i>还差<em>
                                            2226
                                            
                                        </em>票追上前一名</p>
                                        
                                        <div class="icon-box rec">
                                            <span></span>
                                            <b></b>
                                        </div>
                                        <a class="red-radius-btn" id="recBtn" href="javascript:" data-showtype="2" data-eid="qd_G23"><em class="iconfont">&#xe63e;</em>投推荐票</a>
                                    </div>
                                </div>
                            </dd>
                            <dd class="line"></dd>
                            <dd>
                                <h4 class="lang"><span class="act">打赏</span></h4>
                                <div class="action-wrap">
                                    <div class="ticket">
                                        <p>本周打赏人数</p>
                                        <p class="num"><i class="rewardNum" id="rewardNum">12</i></p>
                                        
                                        <p>今日<em id="todayNum">12</em>人打赏</p>
                                        
                                        <div class="icon-box money">
                                            <span></span>
                                            <b></b>
                                        </div>
                                        <a class="red-radius-btn" id="rewardBtn" href="javascript:" data-showtype="3" data-eid="qd_G24"><em class="iconfont">&#xe635;</em>打赏作者</a>
                                        <p class="tip"><cite>100</cite>起点币=<cite>100</cite>点粉丝值</p>
                                    </div>
                                </div>
                            </dd>
                            <dd class="line"></dd>
                            <dd>
                                <h4 class="lang"><span>我的粉丝等级</span></h4>
                                
                                <div class="fans-rank login-out mb20 cf " id="noLogin" data-login="0">
                                    <div class="user-photo fl">
                                        <a href="//me.qidian.com" target="_blank">
                                            <img src="//qidian.gtimg.com/qd/images/ico/default_user.38712.png">
                                        </a>
                                    </div>
                                    <div class="fans-info">
                                        <p><a class="blue" id="login-btn" href="javascript:" data-eid="qd_G28">登录</a>查看粉丝等级</p>
                                    </div>
                                </div>
                                <div class="fans-rank login-in mb20 cf hidden" id="loginIn" data-login="1">
                                    <div class="user-photo fl">
                                        <a href="//me.qidian.com" id="myUserIcon"  target="_blank">
                                            <img src="//qidian.gtimg.com/qd/images/ico/default_user.38712.png">
                                            <span class="user-level" id="userLevel"></span>
                                        </a>
                                    </div>
                                    <div class="fans-info hidden" id="haveLv">
                                        <p>我的排名<b class="red">--</b>名</p>
                                        <p>还差<span id="Lnterval">--</span>粉丝值升级</p>
                                    </div>
                                    <div class="fans-info hidden" id="noLv">
                                        <p>暂无粉丝等级</p>
                                        <p id="levelUp">对本书消费可提升等级</p>
                                    </div>
                                </div>
                                <div class="fans-dynamic">
                                    <h4 class="lang"><span>本书粉丝动态</span></h4>
                                    
                                    <div class="fans-slide-wrap">
                                        <div class="scroll-div" id="scrollDiv">
                                            <ul class="fans-slide">
                                            
                                            <li data-rid="1" class="">
                                                <em class="money"></em><a href="//me.qidian.com/friendIndex.aspx?id=585260" target="_blank" data-eid="" title="恒之">恒之</a><span>打赏</span>100起点币
                                            </li>
                                            
                                            <li data-rid="2" class="">
                                                <em class="money"></em><a href="//me.qidian.com/friendIndex.aspx?id=219769705" target="_blank" data-eid="" title="书友160715014359966">书友160715014359966</a><span>打赏</span>1000起点币
                                            </li>
                                            
                                            <li data-rid="3" class="">
                                                <em class="money"></em><a href="//me.qidian.com/friendIndex.aspx?id=11096319" target="_blank" data-eid="" title="tool53589">tool53589</a><span>打赏</span>100起点币
                                            </li>
                                            
                                            <li data-rid="4" class="">
                                                <em class="money"></em><a href="//me.qidian.com/friendIndex.aspx?id=11096319" target="_blank" data-eid="" title="tool53589">tool53589</a><span>打赏</span>100起点币
                                            </li>
                                            
                                            <li data-rid="5" class="">
                                                <em class="money"></em><a href="//me.qidian.com/friendIndex.aspx?id=216268006" target="_blank" data-eid="" title="啸傲三尺雪">啸傲三尺雪</a><span>打赏</span>100起点币
                                            </li>
                                            
                                            <li data-rid="6" class="">
                                                <em class="month"></em><a href="//me.qidian.com/friendIndex.aspx?id=225969109" target="_blank" data-eid="" title="那一场无涯的梦啊">那一场无涯的梦啊</a><span>投了</span>2张月票
                                            </li>
                                            
                                            <li data-rid="7" class="">
                                                <em class="month"></em><a href="//me.qidian.com/friendIndex.aspx?id=1334285" target="_blank" data-eid="" title="gehuang">gehuang</a><span>投了</span>1张月票
                                            </li>
                                            
                                            <li data-rid="8" class="">
                                                <em class="rec"></em><a href="//me.qidian.com/friendIndex.aspx?id=1334285" target="_blank" data-eid="" title="gehuang">gehuang</a><span>投了</span>4张推荐票
                                            </li>
                                            
                                            <li data-rid="9" class="">
                                                <em class="rec"></em><a href="//me.qidian.com/friendIndex.aspx?id=11042526" target="_blank" data-eid="" title="学生图腾">学生图腾</a><span>投了</span>6张推荐票
                                            </li>
                                            
                                            <li data-rid="10" class="">
                                                <em class="rec"></em><a href="//me.qidian.com/friendIndex.aspx?id=225257337" target="_blank" data-eid="" title="吕小布l">吕小布l</a><span>投了</span>4张推荐票
                                            </li>
                                            
                                            <li data-rid="11" class="">
                                                <em class="rec"></em><a href="//me.qidian.com/friendIndex.aspx?id=309269008" target="_blank" data-eid="" title="黑色天龙下的青春">黑色天龙下的青春</a><span>投了</span>1张推荐票
                                            </li>
                                            
                                            <li data-rid="12" class="">
                                                <em class="rec"></em><a href="//me.qidian.com/friendIndex.aspx?id=212021466" target="_blank" data-eid="" title="岁染00">岁染00</a><span>投了</span>6张推荐票
                                            </li>
                                            
                                            <li data-rid="13" class="">
                                                <em class="month"></em><a href="//me.qidian.com/friendIndex.aspx?id=301865609" target="_blank" data-eid="" title="书友20170517221443099">书友20170517221443099</a><span>投了</span>2张月票
                                            </li>
                                            
                                            <li data-rid="14" class="">
                                                <em class="month"></em><a href="//me.qidian.com/friendIndex.aspx?id=227785322" target="_blank" data-eid="" title="书友170105193138372">书友170105193138372</a><span>投了</span>1张月票
                                            </li>
                                            
                                            <li data-rid="15" class="">
                                                <em class="month"></em><a href="//me.qidian.com/friendIndex.aspx?id=199474314" target="_blank" data-eid="" title="书友150124225445870">书友150124225445870</a><span>投了</span>2张月票
                                            </li>
                                            
                                        </ul>
                                        </div>
                                    </div>
                                    
                                </div>
                            </dd>
                        </dl>
                    </div>
                </div>
                
                <div class="games-op-wrap" data-l1="17">
                    <div class="left-game">
                        
                        <a href="http://cpgame.qd.game.qidian.com/Home/Index/directLogin/name/sslj/way/1?qd_game_key=sslj345x70&amp;qd_dd_p1=528" target="_blank" style="display: block" data-eid="qd_G102" data-qd_dd_p1="1"><img src="//qidian.qpic.cn/qidian_common/349573/c480560d3370c97d032b875b0bea89a7/0"><span class="op-tag"></span></a>
                        
                    </div>
                    <div class="right-game">
                        
                        <a href="http://cpgame.qd.game.qidian.com/Home/Index/directLogin/name/dmbj/way/1?qd_game_key=dmbj345x70&amp;qd_dd_p1=652" target="_blank" style="display: block" data-eid="qd_G103" data-qd_dd_p1="1"><img src="//qidian.qpic.cn/qidian_common/349573/b899f3794e389f4d743aa072af8185da/0"><span class="op-tag"></span></a>
                        
                    </div>
                </div>
                
                
                <div class="like-more mb30 cf" data-l1="6">
                    <h3 class="lang">喜欢这本书的人还喜欢</h3>
                    <div class="like-more-list">
                        <ul class="cf">
                            
                            <li data-rid="1">
                                <div class="book-img" title="大道朝天">
                                    <a href="//book.qidian.com/info/1010496369" target="_blank" data-eid="qd_G30" data-bid="1010496369"><img class="lazy" src="//qidian.gtimg.com/qd/images/common/default_book.5968b.png" data-original="//qidian.qpic.cn/qdbimg/349573/1010496369/90" alt="大道朝天"></a>
                                </div>
                                <h4><a href="//book.qidian.com/info/1010496369" target="_blank" title="大道朝天" data-eid="qd_G29" data-bid="1010496369">大道朝天</a></h4>
                                <p>82%的用户读过</p>
                            </li>
                            
                            <li data-rid="2">
                                <div class="book-img" title="无上崛起">
                                    <a href="//book.qidian.com/info/1010000699" target="_blank" data-eid="qd_G30" data-bid="1010000699"><img class="lazy" src="//qidian.gtimg.com/qd/images/common/default_book.5968b.png" data-original="//qidian.qpic.cn/qdbimg/349573/1010000699/90" alt="无上崛起"></a>
                                </div>
                                <h4><a href="//book.qidian.com/info/1010000699" target="_blank" title="无上崛起" data-eid="qd_G29" data-bid="1010000699">无上崛起</a></h4>
                                <p>90%的用户读过</p>
                            </li>
                            
                            <li data-rid="3">
                                <div class="book-img" title="君临星空">
                                    <a href="//book.qidian.com/info/1010495773" target="_blank" data-eid="qd_G30" data-bid="1010495773"><img class="lazy" src="//qidian.gtimg.com/qd/images/common/default_book.5968b.png" data-original="//qidian.qpic.cn/qdbimg/349573/1010495773/90" alt="君临星空"></a>
                                </div>
                                <h4><a href="//book.qidian.com/info/1010495773" target="_blank" title="君临星空" data-eid="qd_G29" data-bid="1010495773">君临星空</a></h4>
                                <p>75%的用户读过</p>
                            </li>
                            
                            <li data-rid="4">
                                <div class="book-img" title="超凡世界">
                                    <a href="//book.qidian.com/info/1010696572" target="_blank" data-eid="qd_G30" data-bid="1010696572"><img class="lazy" src="//qidian.gtimg.com/qd/images/common/default_book.5968b.png" data-original="//qidian.qpic.cn/qdbimg/349573/1010696572/90" alt="超凡世界"></a>
                                </div>
                                <h4><a href="//book.qidian.com/info/1010696572" target="_blank" title="超凡世界" data-eid="qd_G29" data-bid="1010696572">超凡世界</a></h4>
                                <p>85%的用户读过</p>
                            </li>
                            
                            <li data-rid="5">
                                <div class="book-img" title="尘骨">
                                    <a href="//book.qidian.com/info/1010298084" target="_blank" data-eid="qd_G30" data-bid="1010298084"><img class="lazy" src="//qidian.gtimg.com/qd/images/common/default_book.5968b.png" data-original="//qidian.qpic.cn/qdbimg/349573/1010298084/90" alt="尘骨"></a>
                                </div>
                                <h4><a href="//book.qidian.com/info/1010298084" target="_blank" title="尘骨" data-eid="qd_G29" data-bid="1010298084">尘骨</a></h4>
                                <p>75%的用户读过</p>
                            </li>
                            
                            <li data-rid="6">
                                <div class="book-img" title="大强化">
                                    <a href="//book.qidian.com/info/1010961896" target="_blank" data-eid="qd_G30" data-bid="1010961896"><img class="lazy" src="//qidian.gtimg.com/qd/images/common/default_book.5968b.png" data-original="//qidian.qpic.cn/qdbimg/349573/1010961896/90" alt="大强化"></a>
                                </div>
                                <h4><a href="//book.qidian.com/info/1010961896" target="_blank" title="大强化" data-eid="qd_G29" data-bid="1010961896">大强化</a></h4>
                                <p>74%的用户读过</p>
                            </li>
                            
                        </ul>
                    </div>
                </div>
                
                <div class="user-commentWrap" data-l1="8">
                    <div class="user-comment-wrap book-friend">
                        <div class="comment-head cf">
                            <h3 class="lang">
                                
                                <a class="send blue j_forumBtn" href="//forum.qidian.com/NewForum/Post.aspx?forumId=1004608738" target="_blank" data-eid="qd_G35">我要发帖</a>
                                <a class="comment-btn blue j_commentBtn hidden" id="goComment" href="javascript:" data-comment="1" data-eid="qd_G33">我要评价</a><span class="j_godiscuss act">作品讨论区</span><i class="grey">|</i><span class="j_gocomment" data-eid="qd_G113">书友评价</span></h3>
                            <div class="sort-box hidden" id="sortBox"><a class="act" href="javascript:" data-order="2" data-eid="qd_G31">热门</a><span>·</span><a href="javascript:" data-order="0" data-eid="qd_G32">最新</a><span class="grey">|</span></div>
                        </div>
                      <div class="userCommentWrap"  id="userCommentWrap" data-l1="7">
                          <div class="la-ball-pulse">
                              <span></span>
                              <span></span>
                              <span></span>
                          </div>
                          
                      </div>
                        <div class="user-discuss" id="userDiscuss" data-l1="8">
                            <div class="la-ball-pulse">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                </div>
            
            </div>
            <div class="right-wrap fr">
                
                    <div class="author-state mb10">
                        <div class="author-info">
                            <div class="info-wrap nobt" data-l1="9">
                                <div class="author-photo" id="authorId" data-authorid="4362453">
                                    <a href="//my.qidian.com/author/4362453" target="_blank" data-eid="qd_G38">
                                        <img src="//facepic.qidian.com/qd_face/349573/a4362453/0">
                                    </a>
                                    
                                    <span class="platina">白金</span>
                                    
                                </div>
                                <p><a href="//my.qidian.com/author/4362453" target="_blank">辰东</a>
                                    
                                    <a class="god-light lv3" href="//my.qidian.com/author/light/4362453" title="大神之光：已经有1100人获得" target="_blank" data-eid="qd_G39"></a>
                                    
                                </p>
                                
                                <p class="">阅文集团白金作家，网络文学代表人物之一，中国作协会员。
                                    <cite class="iconfont blue j_infoUnfold" title="展开介绍"></cite>
                                </p>
                                
                            </div>
                            <div class="info-wrap" data-l1="9">
                                <ul class="work-state cf">
                                    <li>
                                        <span class="book"></span>
                                        <p>作品总数</p>
                                        <em>6</em>
                                    </li>
                                    <li>
                                        <span class="word"></span>
                                        <p>累计字数</p>
                                        <em>2341.16万</em>
                                    </li>
                                    <li>
                                        <span class="coffee"></span>
                                        <p>创作天数</p>
                                        <em>4074</em>
                                    </li>
                                </ul>
                            </div>
                            
                            
                            <div class="info-wrap other-works" data-l1="10">
                                <h3 class="lang"><a class="blue" href="//me.qidian.com/authorIndex.aspx?id=4362453" target="_blank" data-eid="qd_G40">更多<em class="iconfont">&#xe621;</em></a>其他作品</h3>
                                    <div class="work-slides cf" id="workSlides">
                                        <ul>
                                            
                                            
                                            <li id="item1" data-rid="1">
                                                <div class="book-img">
                                                    <a href="//book.qidian.com/info/20117" target="_blank" data-eid="qd_G43" data-bid="20117"><img data-src="//qidian.qpic.cn/qdbimg/349573/20117/90"/>
                                                        
                                                    </a>
                                                </div>
                                                <div class="text">
                                                    <h4><a href="//book.qidian.com/info/20117" target="_blank" data-eid="qd_G44" data-bid="20117">不死不灭</a></h4>
                                                    <p class="red"><a href="//www.qidian.com/wuxia" data-eid="qd_G45" target="_blank">武侠</a><i>&#183;</i><em>8.9分</em></p>
                                                    <p>　　一个被称为魔的人，为了生存而苦苦挣扎，最后走上了一条抗天之路……</p>
                                                    <a class="blue-btn add-book" href="javascript:" data-eid="qd_G46" data-bookId="20117" data-bid="20117">加入书架</a>
                                                </div>
                                            </li>
                                            
                                            <li id="item2" data-rid="2">
                                                <div class="book-img">
                                                    <a href="//book.qidian.com/info/63856" target="_blank" data-eid="qd_G43" data-bid="63856"><img data-src="//qidian.qpic.cn/qdbimg/349573/63856/90"/>
                                                        
                                                    </a>
                                                </div>
                                                <div class="text">
                                                    <h4><a href="//book.qidian.com/info/63856" target="_blank" data-eid="qd_G44" data-bid="63856">神墓</a></h4>
                                                    <p class="red"><a href="//www.qidian.com/xuanhuan" data-eid="qd_G45" target="_blank">玄幻</a><i>&#183;</i><em>9.3分</em></p>
                                                    <p>　　一个死去万载岁月的平凡青年从远古神墓中复活而出……　　</p>
                                                    <a class="blue-btn add-book" href="javascript:" data-eid="qd_G46" data-bookId="63856" data-bid="63856">加入书架</a>
                                                </div>
                                            </li>
                                            
                                            <li id="item3" data-rid="3">
                                                <div class="book-img">
                                                    <a href="//book.qidian.com/info/1097850" target="_blank" data-eid="qd_G43" data-bid="1097850"><img data-src="//qidian.qpic.cn/qdbimg/349573/1097850/90"/>
                                                        
                                                    </a>
                                                </div>
                                                <div class="text">
                                                    <h4><a href="//book.qidian.com/info/1097850" target="_blank" data-eid="qd_G44" data-bid="1097850">长生界</a></h4>
                                                    <p class="red"><a href="//www.qidian.com/xuanhuan" data-eid="qd_G45" target="_blank">玄幻</a><i>&#183;</i><em>9.1分</em></p>
                                                    <p>　　世上谁人能不死？　　任你风华绝代，艳冠天下，到头来也是红粉骷髅；任你一代天骄，坐拥万里江山，到头来也终将化成一抔黄土。　　不过，关于长生不死的传说却始终流传于世。　　故老相传，超脱于人世间之外，有一个浩大的长生界……　　</p>
                                                    <a class="blue-btn add-book" href="javascript:" data-eid="qd_G46" data-bookId="1097850" data-bid="1097850">加入书架</a>
                                                </div>
                                            </li>
                                            
                                            <li id="item4" data-rid="4">
                                                <div class="book-img">
                                                    <a href="//book.qidian.com/info/1735921" target="_blank" data-eid="qd_G43" data-bid="1735921"><img data-src="//qidian.qpic.cn/qdbimg/349573/1735921/90"/>
                                                        
                                                    </a>
                                                </div>
                                                <div class="text">
                                                    <h4><a href="//book.qidian.com/info/1735921" target="_blank" data-eid="qd_G44" data-bid="1735921">遮天</a></h4>
                                                    <p class="red"><a href="//www.qidian.com/xianxia" data-eid="qd_G45" target="_blank">仙侠</a><i>&#183;</i><em>9.3分</em></p>
                                                    <p>　　
　　冰冷与黑暗并存的宇宙深处，九具庞大的龙尸拉着一口青铜古棺，亘古长存。
　　这是太空探测器在枯寂的宇宙中捕捉到的一幅极其震撼的画面。
　　九龙拉棺，究竟是回到了上古，还是来到了星空的彼岸？
　　一个浩大的仙侠世界，光怪陆离，神秘无尽。热血似火山沸腾，激情若瀚海汹涌，欲望如深渊无止境……
　　登天路，踏歌行，弹指遮天。
　　</p>
                                                    <a class="blue-btn add-book" href="javascript:" data-eid="qd_G46" data-bookId="1735921" data-bid="1735921">加入书架</a>
                                                </div>
                                            </li>
                                            
                                            <li id="item5" data-rid="5">
                                                <div class="book-img">
                                                    <a href="//book.qidian.com/info/2952453" target="_blank" data-eid="qd_G43" data-bid="2952453"><img data-src="//qidian.qpic.cn/qdbimg/349573/2952453/90"/>
                                                        
                                                    </a>
                                                </div>
                                                <div class="text">
                                                    <h4><a href="//book.qidian.com/info/2952453" target="_blank" data-eid="qd_G44" data-bid="2952453">完美世界</a></h4>
                                                    <p class="red"><a href="//www.qidian.com/xuanhuan" data-eid="qd_G45" target="_blank">玄幻</a><i>&#183;</i><em>9.3分</em></p>
                                                    <p>　　一粒尘可填海，一根草斩尽日月星辰，弹指间天翻地覆。　　群雄并起，万族林立，诸圣争霸，乱天动地。问苍茫大地，谁主沉浮？！　　一个少年从大荒中走出，一切从这里开始……　　</p>
                                                    <a class="blue-btn add-book" href="javascript:" data-eid="qd_G46" data-bookId="2952453" data-bid="2952453">加入书架</a>
                                                </div>
                                            </li>
                                            
                                        </ul>
                                        <div class="nav">
                                            
                                            <a href="#item1"></a>
                                            
                                            <a href="#item2"></a>
                                            
                                            <a href="#item3"></a>
                                            
                                            <a href="#item4"></a>
                                            
                                            <a href="#item5"></a>
                                            
                                        </div>
                                        
                                        <div class="arrows ">
                                            <a href="javascript:" class="iconfont prev" data-type="prev" data-eid="qd_G41">&#xe628;</a>
                                            <a href="javascript:" class="iconfont next" data-type="next" data-eid="qd_G42">&#xe621;</a>
                                        </div>
                                </div>
                            </div>
                            
                            
                        </div>
                    </div>
                
                    
                
                    <div class="book-list-wrap mb10" data-l1="13">
   <div class="strongrec-list">
       <h3 class="wrap-title lang">本周强推<i>&#183;</i>玄幻</h3>
       <div class="book-list">
           <ul>
               
               <li data-rid="1">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=8" target="_blank" data-eid="qd_G52"><em>「</em>东方玄幻<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011917232" target="_blank" data-eid="qd_G51" data-bid="1011917232" title="写书证道">写书证道</a></strong>
               </li>
               
               <li data-rid="2">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=8" target="_blank" data-eid="qd_G52"><em>「</em>东方玄幻<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011987572" target="_blank" data-eid="qd_G51" data-bid="1011987572" title="仙魔地球">仙魔地球</a></strong>
               </li>
               
               <li data-rid="3">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=8" target="_blank" data-eid="qd_G52"><em>「</em>东方玄幻<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1012019651" target="_blank" data-eid="qd_G51" data-bid="1012019651" title="命运之眼">命运之眼</a></strong>
               </li>
               
               <li data-rid="4">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=8" target="_blank" data-eid="qd_G52"><em>「</em>东方玄幻<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011932535" target="_blank" data-eid="qd_G51" data-bid="1011932535" title="诸天我为帝">诸天我为帝</a></strong>
               </li>
               
               <li data-rid="5">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=8" target="_blank" data-eid="qd_G52"><em>「</em>东方玄幻<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011776258" target="_blank" data-eid="qd_G51" data-bid="1011776258" title="垂钓三千界">垂钓三千界</a></strong>
               </li>
               
               <li data-rid="6">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=8" target="_blank" data-eid="qd_G52"><em>「</em>东方玄幻<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011729513" target="_blank" data-eid="qd_G51" data-bid="1011729513" title="药草供应商">药草供应商</a></strong>
               </li>
               
               <li data-rid="7">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=73" target="_blank" data-eid="qd_G52"><em>「</em>异世大陆<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011827166" target="_blank" data-eid="qd_G51" data-bid="1011827166" title="造神手术师">造神手术师</a></strong>
               </li>
               
               <li data-rid="8">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=78" target="_blank" data-eid="qd_G52"><em>「</em>高武世界<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011877424" target="_blank" data-eid="qd_G51" data-bid="1011877424" title="无限技能升级">无限技能升级</a></strong>
               </li>
               
               <li data-rid="9">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=8" target="_blank" data-eid="qd_G52"><em>「</em>东方玄幻<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011832263" target="_blank" data-eid="qd_G51" data-bid="1011832263" title="恶魔就在身边">恶魔就在身边</a></strong>
               </li>
               
               <li data-rid="10">
                   <a class="channel" href="//www.qidian.com/all?chanId=21&amp;subCateId=8" target="_blank" data-eid="qd_G52"><em>「</em>东方玄幻<em>」</em></a><strong><a class="name" href="//book.qidian.com/info/1011824314" target="_blank" data-eid="qd_G51" data-bid="1011824314" title="两个系统闯仙界">两个系统闯仙界</a></strong>
               </li>
               
           </ul>
       </div>
   </div>
</div>
                
                
                <div class="right-op-wrap mb10" data-l1="18">
                    
                    <a href="http://cpgame.qd.game.qidian.com/Home/Index/directLogin/name/sslj/way/1?qd_game_key=sslj250x174&amp;qd_dd_p1=1824" target="_blank" style="display: block" data-eid="qd_G105" data-qd_dd_p1="1"><img src="//qidian.qpic.cn/qidian_common/349573/6a6d8c95f89fc324a73e8d972e6d5ae7/0"><span class="op-tag"></span></a>
                    
                </div>
                
                <div class="fansRankWrap mb10" id="fansRankWrap" data-l1="12">
                       <div class="la-ball-pulse">
                           <span></span>
                           <span></span>
                           <span></span>
                       </div>
                </div>
                <div class="topFansWrap mb10" id="topFansWrap" data-l1="12">
                    <div class="la-ball-pulse">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
                <div class="break-rules-report cf">
                    <i class="icon-warning"></i>
                    <a href="//jubao.yuewen.com" target="_blank">举报违规有奖</a>
                </div>
                
            </div>
        </div>
        
    </div>
    <div class="footer">
    <div class="box-center cf">
        <div class="friend-link">
            <em><a class="yuewen" href="//www.yuewen.com" target="_blank">阅文集团</a><cite>旗下网站：</cite></em>
                <a href="//www.qidian.com">起点中文网</a>
                <a href="//www.qdmm.com" target="_blank">起点女生网</a>
                <a href="http://chuangshi.qq.com" target="_blank">创世中文网</a>
                <a href="http://yunqi.qq.com" target="_blank">云起书院</a>
                <!--<a href="http://www.rongshuxia.com" target="_blank">榕树下</a>-->
                <a href="//www.hongxiu.com" target="_blank">红袖添香</a>
                <a href="//www.readnovel.com" target="_blank">小说阅读网</a>
                <a href="//www.xs8.cn" target="_blank">言情小说吧</a>
                <a href="http://www.xxsy.net" target="_blank">潇湘书院</a>
                <a href="http://www.tingbook.com" target="_blank">天方听书网</a>
                <a href="http://www.lrts.me" target="_blank">懒人听书</a>
                <a href="http://yuedu.yuewen.com" target="_blank">阅文悦读</a>
                <a href="//www.yuewen.com/app.html#appqq" target="_blank">QQ阅读</a>
                <a href="//www.yuewen.com/app.html#appqd" target="_blank">起点读书</a>
                <a href="//www.yuewen.com/app.html#appzj" target="_blank">作家助手</a>
                <a href="//www.webnovel.com" target="_blank" title="Qidian International">起点国际版</a>
        </div>
        <div class="footer-menu dib-wrap">
            <a href="//www.qidian.com/about/intro" target="_blank">关于起点</a>
            <a href="//www.qidian.com/about/contact" target="_blank">联系我们</a>
            <a href="//join.yuewen.com" target="_blank">加入我们</a>
            <a href="//www.qidian.com/help/index/2" target="_blank">帮助中心</a>
            <a href="#" class="advice" target="_blank">提交建议</a>
            <!--<a href="http://bbs.qidian.com" target="_blank">起点论坛</a>-->
            <a href="http://comic.qidian.com" target="_blank">动漫频道</a>
            <a href="//jubao.yuewen.com" target="_blank">举报中心</a>
        </div>
        <div class="copy-right">
            <p><span>Copyright &copy; 2002-2018 www.qidian.com All Rights Reserved</span>版权所有 上海玄霆娱乐信息科技有限公司</p>
            <p>上海玄霆娱乐信息科技有限公司 增值电信业务经营许可证沪B2-20080046 出版经营许可证 新出发沪批字第U3718号 沪网文[2015]0081-031 新出网证（沪）字010 沪ICP备08017520号-1</p>
            <p>请所有作者发布作品时务必遵守国家互联网信息管理办法规定，我们拒绝任何色情小说，一经发现，即作删除！举报电话：010-59357051</p>
            <p>本站所收录的作品、社区话题、用户评论、用户上传内容或图片等均属用户个人行为。如前述内容侵害您的权益，欢迎举报投诉，一经核实，立即删除，本站不承担任何责任</p>
            <p>联系方式 总机 021-61870500 地址：中国（上海）自由贸易试验区碧波路690号6号楼101、201室</p>
        </div>
        
    </div>
</div>

</div>
<script>
    // 全局的通用数据都放g_data变量里
    var g_data = {};
    // 环境变量，会按照环境选择性打log
    g_data.envType = 'pro';
    // 用作统计PV
    var directCatalog = location.hash;
    //如果hash中有catalog，则优先展示目录页
    if (directCatalog.indexOf('Catalog') > 0) {
        g_data.pageId = 'qd_P_mulu';
    }else{
        g_data.pageId = 'qd_P_xiangqing';
    }
    // 当前页面路由
    g_data.domain = '//book.qidian.com';
    //环境域名
    g_data.domainSearch = 'www.qidian.com/search';
    //静态资源域名
    g_data.staticPath = '//qidian.gtimg.com/qd';
    
        //广告区flash标识
        g_data.gamesFlashOp = {
            middleLeft1:1,
                middleLeft2:1,
                middleRight:1
        };
        //是否是推广图
        g_data.isRecom = 0;
    
    g_data.salesMode = 1;
    g_data.pageJson = {
    
        // 是否是VIP书籍，传入js，在弹窗时需要判断，如果不是VIP看不到月票Tab
        isVip:1,
        // 是否签约作品，传入js，EJS后加载模板判断是否显示
        isSign:1,
        // 是否出版物，传入js，EJS后加载模板判断是否显示
        isPublication: false,
        // 是否出版物，传入js，EJS后加载模板判断是否显示
        salesMode: 1,
        // 是否要送月票 传入js， EJS后加载模板判断使用
        noRewardMonthTic:0,
    
        // 是否已登录，传入js，EJS后加载模板判断是否显示
        isLogin:0,
        // 获得bookId的json格式，传入js，EJS后加载模板中可以直接使用
        bookId:1004608738,
        // 获得签约状态，传入js，EJS后加载弹窗下载使用
        signStatus:'Ａ级签约',
        //作家专区链接环境变量传入EJS模板
        mePreFix:'//me.qidian.com',
        //讨论区连接环境变量传入EJS模板
        forumPreFix:'//forum.qidian.com',
        //判断男女生网
        bookType:1,
        // author
        authorInfo: {
            authorId: '4362453',
            authorName: '辰东',
            avatar: '//facepic.qidian.com/qd_face/349573/a4362453/0'
        }
    }
    //判断男女生网状态 0和1
    g_data.isWebSiteType = 1;
    g_data.hasDirectData = 0;
    //获取讨论区数据的参数之一
    g_data.chanId = 21;
    // 新书预发数据
    g_data.isPre = false;
    g_data.preTimeLeft = NaN;
</script>

<script>
    (function(){
        var bp = document.createElement('script');
        var curProtocol = window.location.protocol.split(':')[0];
        if (curProtocol === 'https') {
            bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
        }
        else {
            bp.src = 'http://push.zhanzhang.baidu.com/push.js';
        }
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(bp, s);
    })();
</script>

<script data-ignore="true" src="//qidian.gtimg.com/lbf/1.0.4.2/LBF.js?max_age=31536000"></script>
<script>
    // LBF 配置
    LBF.config({"paths":{"site":"//qidian.gtimg.com/qd/js","qd":"//qidian.gtimg.com/qd","common":"//qidian.gtimg.com/common/1.0.0"},"vars":{"theme":"//qidian.gtimg.com/qd/css"},"combo":true,"debug":false});
    LBF.use(['lib.jQuery'], function ($) {
        window.$ = $;
    });
</script>
<script>
    LBF.use(['monitor.SpeedReport', 'qd/js/component/login.a4de6.js', 'qd/js/book_details/index.3ad4f.js' ], function (SpeedReport, Login, Index) {
        // 页面逻辑入口
        if(Login){
            Login.init().always(function(){
                Index && typeof Index === 'function' && new Index();
            })
        }
        if(219 && 219 != ''){
            $(window).on('load.speedReport', function () {
                // speedTimer[onload]
                speedTimer.push(new Date().getTime());
                var f1 = 7718, // china reading limited's ID
                        f2 = 219, // site ID
                        f3 = 37; // page ID
                // chrome & IE9 Performance API
                SpeedReport.reportPerformance({
                    flag1: f1,
                    flag2: f2,
                    flag3IE: f3,
                    flag3Chrome: f3,
                    rate:0.1,
                    url: '//isdspeed.qidian.com/cgi-bin/r.cgi'
                });
                // common speedTimer:['dom ready', 'onload']
                var speedReport = SpeedReport.create({
                    flag1: f1,
                    flag2: f2,
                    flag3: f3,
                    start: speedZero,
                    rate:0.1,
                    url: '//isdspeed.qidian.com/cgi-bin/r.cgi'
                });
                // chrome & IE9 Performance API range 1~19, common speedTimer use 20+
                for (var i = 0; i < speedTimer.length; i++) {
                    speedReport.add(speedTimer[i], i + 20)
                }
                // http://isdspeed.qq.com/cgi-bin/r.cgi?flag1=7718&flag2=224&flag3=1&1=38&2=38&…
                speedReport.send();
            })
        }
    });
    speedTimer.push(new Date().getTime());
</script>

<script>
    var _mtac = {};
    (function() {
        var mta = document.createElement("script");
        mta.src = "//pingjs.qq.com/h5/stats.js?v2.0.2";
        mta.setAttribute("name", "MTAH5");
        mta.setAttribute("sid", "500451537");
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(mta, s);
    })();
</script>

</body>
</html>

"""

def test_qidian_novel_info():
    url = 'http://book.qidian.com/info/1004608738'
    item_data = QidianNovelInfoItem.get_item(html=HTML)

    assert item_data['novel_name'] == '圣墟'
