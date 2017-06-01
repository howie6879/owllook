## talonspider

### 1.为什么写这个？

针对owllook这个项目的小说排行榜，不想动用比较重的框架来进行爬取。

因此针对这个需求写了`talonspider`:

- 1.针对单页面的item提取

### 2.介绍

#### 2.1.item

目标值提取类，当时是看[demiurge](https://github.com/matiasb/demiurge)这个项目研究了下`metaclass`，可以说item部分是参考这个的。

`item`的目的是是提取目标值，默认需要提供html或者对应的url才会返回自定义的field（写scrapy应该很清楚要先在item定义field吧），利用lxml解析。

就算没有爬虫模块，这个部分是可以单独使用的，目的时针对当爬取到目标页面那层的时候，进行目标数据的提取，当前目标数据的提取情况分两种：

##### 2.1.1.单一目标

比如这个网址http://book.qidian.com/info/1004608738

提取的对象很明确，这么多字段是一次结果，即一个页面一个目标，称之为单一目标获取，字段如下：

|        field        |     css_select     |
| :-----------------: | :----------------: |
|        title        |  .book-info>h1>em  |
|       author        |      a.writer      |
|        cover        |   a#bookImg>img    |
|      abstract       |  div.book-intro>p  |
|         tag         |     span.blue      |
|   latest_chapter    | div.detail>p.cf>a  |
| latest_chapter_time | div.detail>p.cf>em |

使用起来很简单：

```python
# 引入模块
import time
from owllook.utils.talonspider import Item, TextField, AttrField
from pprint import pprint

# 定义目标field
class TestSpider(Item):
    title = TextField(css_select='.book-info>h1>em')
    author = TextField(css_select='a.writer')
    # 当提取的值是属性的时候，要定义AttrField
    cover = AttrField(css_select='a#bookImg>img', attr='src')
    abstract = TextField(css_select='div.book-intro>p')
    tag = TextField(css_select='span.blue')
    latest_chapter = TextField(css_select='div.detail>p.cf>a')
    latest_chapter_time = TextField(css_select='div.detail>p.cf>em')
	
    # 这里可以二次对获取的目标值进行处理，比如替换、清洗等
    def tal_title(self, title):
        # Clean your target value
        return title

    def tal_cover(self, cover):
        return 'http:' + cover
	
    # 当目标值的对象只有一个，默认将只提取出来，否则返回list，可以在这里定义一个函数进行循环提取
    def tal_tag(self, ele_tag):
        return '#'.join([i.text for i in ele_tag])

    def tal_latest_chapter_time(self, latest_chapter_time):
        return latest_chapter_time.replace('今天', str(time.strftime("%Y-%m-%d ", time.localtime())))

# 获取值
item_data = TestSpider.get_item(url='http://book.qidian.com/info/1004608738')
pprint(item_data)

# output
# {'abstract': '在破败中崛起，在寂灭中复苏。',
#  'author': '辰东',
#  'cover': 'http://qidian.qpic.cn/qdbimg/349573/1004608738/180',
#  'latest_chapter': '求下月票啦，请投来吧',
#  'latest_chapter_time': '2017-06-01 01:19更新',
#  'spider_name': 'testspider',
#  'tag': '连载#签约#VIP',
#  'title': '圣墟'}
```

写个类继承自Item就搞定了，ok

##### 2.1.2.循环目标

比如https://movie.douban.com/top250

这个页面每页展示25部电影，我的爬虫目标就是每页的25部电影信息，所以这个目标页的目标数据是多个item的，对于这种情况，目标是需要循环获取的。