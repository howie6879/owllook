/*
Created By MSCSTSTS
2017-09-27 18:13:50 UTC+8


Edit By MSCSTSTS
2017-12-02 19:36:17 UTC+8
+触屏滑动切换上一章/下一章。
+键盘左右方向键切换上一章/下一章。

*/


//--------------------------------------------------------------------------------------------

/*
登录、书签、加入书库等功能，都是基于刷新或者ajax
所以仅需修改部分页面
最后，将页面滑动到顶部即可。
处理逻辑：
	1：页面加载，检查浏览器是否支持 ajax 和 sessionStorage
	2：查询下一章 和 上一章是否已被缓存，若没有，则进行 ajax 请求，并将对应页面存入sessionStorage
	3：点击上一章或下一章按钮以后，将缓存中的数据取出，重新渲染页面，回到顶部，修改浏览器url，并重新执行2
需要缓存的条目：
	1：本页链接      data.url
	2：下一章链接  data.next_chapter."下一章"
	3：上一章链接  data.next_chapter."上一章"
	4：章节名         data.name
	5：小说名         data.novels_name
	6：正文内容      data.soup
	7：是否书签      data.bookmark
需要更新的页面内容：
	0：【索引项】 页面链接（相对地址）    由 缓存数据的本页链接 拼接产生
	1：书签状态          #bookMark   的 class ，根据 缓存数据 的 是否书签来定义 class
	2：隐藏表单          page_url  的 value       , 根据 缓存数据 的 本页链接
	3：页面标题          page_title          ,  根据 缓存数据 的 章节名产生
	4：正文文本          page_chapter_content      ,根据 缓存数据 的 正文内容产生
	5：上一章和下一章的地址     ，根据缓存数据的上一章链接和下一章链接产生
	6：地址栏URL ，使用replaceState来更新，根据缓存数据的 本页链接 来拼接
*/


$(document).ready(function () {

    var page_btn_pre = $("div.pre_next > a:nth-child(1)");
    var page_btn_next = $("div.pre_next > a:nth-child(2)");
    var page_title = $("title");
    var page_chapter_name = $("#content_name");
    // var page_chapter_content = $(".show-content>div");//正文
    var page_chapter_content = $($(".show-content").children("*").get(0)); //正文
    var page_bookmark = $("#bookMark");//书签，需要修改样式
    var page_url = $("#url");//页面隐藏表单，本页地址

    function get_chapter(n_url) {
        $.ajax({
            //提交数据的类型 POST GET
            type: "GET",
            //提交的网址
            url: n_url,
            //提交的数据
            data: {is_ajax: "owl_cache"},
            //返回数据的格式
            datatype: "json",//"xml", "html", "script", "json", "jsonp", "text".
            //在请求之前调用的函数
            //beforeSend:function(){$("#msg").html("logining");},
            //成功返回之后调用的函数
            success: function (data) {
                if (typeof data.name == "undefined") {

                } else { // 正确获取到数据
                    var obj = {
                        url: data.url,
                        pre_chapter_url: transform(data.next_chapter)[0],
                        next_chapter_url: transform(data.next_chapter)[1],
                        name: data.name,
                        novels_name: data.novels_name,
                        content: data.soup,
                        bookmark: data.bookmark,
                        chapter_url: data.chapter_url
                    };
                    store(n_url, obj);
                }
            },
            //调用执行后调用的函数
            complete: function () {

            },
            //调用出错执行的函数
            error: function () {
                //请求出错处理
            }
        });
    }

    function transform(obj) {
        var arr = [];
        for (var item in obj) {
            arr.push(obj[item]);
        }
        return arr;
    }

    function store(n_url, obj) {
        window.sessionStorage.setItem(n_url, JSON.stringify(obj));
    }

    function ajax_content_init() {
        if (isSupport()) {
            log("支持sessionStorage，将为你开启页面缓存");
            search_url = window.location;
            // 来自书签页面的跳转不进行缓存
            if (search_url.search.indexOf("from_bookmarks") > 0) {
                log('来自书签页面的跳转不进行缓存')
            } else {
                ajax_task();
                page_bookmark.bind("click", function () {
                    cache_reset();
                });
            }
        } else {
            //不支持
            return;
        }
    }

    function ajax_task() {
        store_query();//检查是否已缓存
        page_btn_pre.unbind("click");
        page_btn_pre.click(function () {
            event.preventDefault();
            if (window.sessionStorage.getItem(page_btn_pre.attr("href")) === null) {
                //若未缓存
                window.location.href = page_btn_pre.attr("href");
            } else {
                try {
                    load(page_btn_pre.attr("href"));
                } catch (err) {
                    window.location.href = page_btn_pre.attr("href");
                }

            }
        });
        page_btn_next.unbind("click");
        page_btn_next.click(function () {
            event.preventDefault();
            if (window.sessionStorage.getItem(page_btn_next.attr("href")) === null) {
                //若未缓存
                window.location.href = page_btn_next.attr("href");
            } else {
                try {
                    load(page_btn_next.attr("href"));
                } catch (err) {
                    window.location.href = page_btn_next.attr("href");
                }

            }
        });
    }


    function load_bookmark(data) {
        page_bookmark.removeClass("bookMark");
        page_bookmark.removeClass("bookMarkAct");
        //log(data.bookmark);
        if (data.bookmark == 0) {
            page_bookmark.addClass("bookMark");
        } else {
            page_bookmark.addClass("bookMarkAct");
        }
    }

    function load_hiddenForm(data) {
        page_url.val(data.url);
    }

    function load_title(data) {
        page_title.html(data.name + " - owllook");
    }

    function stripscript(s) {//用于过滤script标签
        return s.replace(/<script>.*?<\/script>/ig, '').replace(/<.*?div.*?>/, '');
    }

    function load_chapter_content(data) {
        page_chapter_content.html(stripscript($(data.content).html()));
    }

    function load_chapter_name(data) {
        page_chapter_name.text(data.name);
    }

    function load_btn_href(data) {
        page_btn_pre.attr("href", "/owllook_content?url=" + data.pre_chapter_url + "&chapter_url=" + data.chapter_url + "&novels_name=" + data.novels_name);
        page_btn_next.attr("href", "/owllook_content?url=" + data.next_chapter_url + "&chapter_url=" + data.chapter_url + "&novels_name=" + data.novels_name);
    }

    function load_location_url(data) {
        var th_url = window.location.href + "";
        var pos = th_url.indexOf("/owllook_content?");
        var td_url = "/owllook_content?url=" + data.url + "&name=" + data.name + "&chapter_url=" + data.chapter_url + "&novels_name=" + data.novels_name;
        th_url += td_url;
        //log(th_url);
        window.history.replaceState({}, data.name + " - owllook", td_url);
    }

    function load(index) {//从缓存中加载内容
        var data = JSON.parse(window.sessionStorage.getItem(index));
        load_bookmark(data);
        load_hiddenForm(data);
        load_title(data);
        load_chapter_content(data);
        load_chapter_name(data);
        load_btn_href(data);
        load_location_url(data);
        $("body > div.container.all-content > div.move > div.move_up").click();//回到顶部
        ajax_task();
    }


    function store_query() {
        var pre_url = page_btn_pre.attr("href");
        var next_url = page_btn_next.attr("href");
        //log(pre_url);
        //log(window.sessionStorage.getItem(pre_url));
        if (window.sessionStorage.getItem(pre_url) === null) {
            get_chapter(pre_url);
        }
        if (window.sessionStorage.getItem(next_url) === null) {
            get_chapter(next_url);
        }
    }

    function cache_reset() {
        window.sessionStorage.clear();
        ajax_task();
    }


    function isSupport() {
        if (typeof window.sessionStorage == "undefined") { //判断是否支持sessionStorage
            return false;
        }
        return true;
    }


    function log(s) {
        if (1) {
            console.log(s);
        }

    }


    ajax_content_init();


    /*
        2017年12月2日 +触屏滑动切换上一章/下一章。
    */
    //按键事件
    $(document).keydown(function (event) {
        var e = event || window.event;
        var k = e.keyCode || e.which;
        switch (k) {
            case 39:
                // right
                page_btn_next.click();
                break;
            case 37:
                // left
                page_btn_pre.click();
                break;
            case 38:
                //	up
                break;
            case 40:
                // down
                break;
        }
        return true;
    });

    // (function(){
    // 	var startX,startY,endX,endY;
    // 	var el = document.querySelector("body");
    // 	//获取点击开始的坐标
    // 	el.addEventListener("touchstart", function (e){
    // 		startX = e.touches[0].pageX;
    // 		startY = e.touches[0].pageY;
    // 	});
    // 	//获取点击结束后的坐标
    // 	el.addEventListener("touchend", function(e){
    // 		endX = e.changedTouches[0].pageX;
    // 		endY = e.changedTouches[0].pageY;
    // 		var x = (endX - startX);
    // 		var y = (endY - startY);
    // 		if(Math.abs(x/y)>5&&Math.abs(x)>30){
    // 			if(x<0){
    // 				page_btn_next.click();
    // 			}else{
    // 				page_btn_pre.click();
    // 			}
    // 		}
    //
    // 	});
    // })();
});


//---------------------------------------------------------------------------------------