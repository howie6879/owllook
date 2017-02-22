### 

### 网络小说搜索引擎（novels-search）

### 1.说明

`novels-search`是一个基于其他网站的垂直小说搜索引擎，至于为什么写这个，一个是想利用`sanic`尽量做成异步服务，二是想就此练习下推荐系统。

- sanic：基于Python 3.5+的异步web服务器，快快快。
- vloop：sanic默认使用uvloop，替代asyncio本身的loop
- motor：异步的mongodb驱动


对于不同网站的小说，页面规则都不尽相同，我希望能够在代码解析后再统一展示出来，这样方便且美观，而不是仅仅跳转到对应网站就完事，清新简洁的阅读体验才是最重要的。

目前采用的是直接在百度上进行结果检索，也不是不能做的更大更全，只是觉得没什么意义，目前的检索结果已经很足够。

我尽量写少量的规则来完成解析，具体见[规则定义](https://github.com/howie6879/novels-search/blob/master/docs/%E8%A7%84%E5%88%99%E5%AE%9A%E4%B9%89.md)，遇到自己喜欢的小说网站，你也可以自己添加解析。

BTW，sanic写界面确实不是很方便。

**运行：**

`python novels_search/server.py`

### 2.demo

具体效果图请看下面：

目录解析：

![chapter](./docs/chapter.png)



章节内容解析：

![chapter](./docs/content.png)

