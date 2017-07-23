![owllook-demo](http://oe7yjec8x.bkt.clouddn.com/howie/2017-03-08-owllook.gif)
## 0.前言
事情的起因是这样的，前段时间在把之前写的一些同步网络请求代码改成异步的，用的是`aiohttp`，既然是请求，那请求什么呢，就百度吧，请求什么内容呢，我随手一输自己最近看的一本小说，然后作为练手用，就做了这个，我将其取名为`owllook`，准备做成一个推荐系统，所以我就将其部署上去，这才有了这个网站。

上一篇介绍了自己在使用`sanic`过程中遇到的一些问题，这次就想介绍下这个[owllook--novels_search](https://github.com/howie6879/novels-search)，上面是演示demo，具体可以见[http://www.owllook.net/](http://www.owllook.net/)
**本项目纯属共享学习之用，不得用于商业！**
首先我想说下目前的项目进度：

v0.1已经上线：

- 小说的基本搜索解析功能
- 搜索记录
- 缓存
- 书架
- 书签
- 登录（**暂时不开放注册，可与我申请体验**）

TODO:

- [ ] 注册
- [ ] 阅读书单
- [ ] 手机端兼容
- [ ] 推荐
- [ ] 排行榜
- [ ] 个人中心

## 1.介绍
`owllook`的思路很简单，利用百度检索出来的结果，进行过滤解析后再展示，使用的技术如下：

- sanic：基于Python 3.5+的异步web服务器，快快快
- sanic_session：sanic的持续会话插件
- vloop：sanic默认使用uvloop，替代asyncio本身的loop
- motor：异步的mongodb驱动
- aiohttp：异步请求
- aiocache：异步缓存，本项目改用了其中的decorator部分，缓存数据库使用redis

对于用户的一系列操作信息，使用`mongodb`进行存储，而缓存则使用`redis`。

对于不同网站的小说，页面规则都不尽相同，我希望能够在代码解析后再统一展示出来，这样方便且美观，而不是仅仅跳转到对应网站就完事，清新简洁的阅读体验才是最重要的。

目前采用的是直接在百度上进行结果检索，也不是不能做的更大更全，只是觉得没什么意义，目前的检索结果已经很足够。

我尽量写少量的规则来完成解析，具体见[规则定义](https://github.com/howie6879/novels-search/blob/master/docs/%E8%A7%84%E5%88%99%E5%AE%9A%E4%B9%89.md)，遇到自己喜欢的小说网站，方便诸位添加解析。

一般都是在下班时间编写这个项目，目前`v0.1`版本大概实现。

后期我准备将基础功能写好之后，能够实现小说与kindle之间的对接。

## 2.解析
这个项目的思路与技术都比较简单，但是小说网站的解析工作是很难全部解析完毕，下面我将举个例子怎么具体的解析一个网站，欢迎各位添砖加瓦，请先看一遍[规则定义](https://github.com/howie6879/novels-search/blob/master/docs/%E8%A7%84%E5%88%99%E5%AE%9A%E4%B9%89.md)。
解析也很简单，只要求有点html以及css基础即可。

首先进入网站http://www.owllook.net/。
搜索：
![01](http://oe7yjec8x.bkt.clouddn.com/howie/2017-03-10-01.png-blog.howie)

注意第一条结果显示未解析，这就是我们要解析的对象了，点击进入源网站，审查小说目录对应的元素，这里显示的是：`class="mulu_list`，然后注意其`content_url`类型是`0`
![02](http://oe7yjec8x.bkt.clouddn.com/howie/2017-03-10-02.png-blog.howie)

进入小说章节内容页面，审查元素可以看到`id=htmlContent`，所以`content_selector=htmlContent`

接下来进入项目，打开`config/rules.py`文件，在RULES字典中加入：

``` python
'www.ybdu.com': Rules('0', {'class': 'mulu_list'}, {'id': 'htmlContent'}),
```
这时候再重启服务，刷新页面：
![03](http://oe7yjec8x.bkt.clouddn.com/howie/2017-03-10-03.png-blog.howie)
可以看到未解析变成了已解析，这时候点击进入，会出现两种情况：

- 排版完整，不需要再写样式，此时请直接解析章节内容
- 排版不行，需要写样

现在我演示的这个链接排版就是显示不行，请打开`/static/novels/css/chapter.css`文件，在编写之前，请先看下面这张图：
![04](http://oe7yjec8x.bkt.clouddn.com/howie/2017-03-10-04.jpeg-blog.howie)

图中.mulu_list1：打错了表示区域1，.mulu_list1：表示区域3.

首先更改区域1的样式，我已经在代码注释写了各个区域样式代码在哪，直接更改就行，比如：

``` css
/* 区域1 */
.mulu_list, .acss, .list, #xslist ul, .dirlist, .list-chapter, .list_box ul, #defaulthtml4 table, .article-list > dl, .update, #list .box, .bookcontent > dl, .listmain > dl, .ml_main > dl, #list dl, #chapter_list, .chapterlist, tbody, .mt10, .catalog, #readerlists {
    float: left;
    overflow: hidden;
    padding-bottom: 1px;
    margin: auto;
    background: #F6F4EC;
    border-radius: 15px;
}
```
可以看到加上了`.mulu_list`，以此类推，最后解析完毕之后如下图：
![05](http://oe7yjec8x.bkt.clouddn.com/howie/2017-03-10-05.png-blog.howie)

注意章节内容里面一些无关的链接以及原本网页自带的上一章下一章需要隐藏掉哦。

## 3.总结
功能还很简单，解析的网站有很多，希望各位添砖加瓦，容我奉上项目地址：[owllook--novels_search](https://github.com/howie6879/novels-search)

**仅供分享交流  不可用于商业用途**


