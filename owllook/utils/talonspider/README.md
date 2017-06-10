## talonspider

### 1.为什么写这个？

针对owllook这个项目的小说排行榜，不想动用比较重的框架来进行爬取。

因此针对这个需求写了`talonspider` [已经单独出来成为一个包]:

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
	
    # 当目标值的对象只有一个，默认将值提取出来，否则返回list，可以在这里定义一个函数进行循环提取
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

我在`item`中限制了一点，当你定义的爬虫类需要在某一页面循环获取你的目标时，则需要定义`target_item`属性。

对于豆瓣250这个页面，我们的目标是25部电影信息，所以该这样定义：

|      field      |  css_select   |
| :-------------: | :-----------: |
| target_item（必须） |   div.item    |
|      title      |  span.title   |
|      cover      | div.pic>a>img |
|    abstract     |   span.inq    |



```python
# 定义继承自item的爬虫类
class DoubanSpider(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    def tal_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])
        
items_data = DoubanSpider.get_items(url='https://movie.douban.com/top250')
result = []
for item in items_data:
    result.append({
        'title': item.title,
        'cover': item.cover,
        'abstract': item.abstract,
    }
pprint(result)
# 搞定输出
# [{'abstract': '希望让人自由。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p480747492.jpg',
#   'title': '肖申克的救赎/The Shawshank Redemption'},
#  {'abstract': '怪蜀黍和小萝莉不得不说的故事。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p511118051.jpg',
#   'title': '这个杀手不太冷/Léon'},
#  {'abstract': '风华绝代。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1910813120.jpg',
#   'title': '霸王别姬'},
#  {'abstract': '一部美国近现代史。',
#   'cover': 'https://img1.doubanio.com/view/movie_poster_cover/ipst/public/p510876377.jpg',
#   'title': '阿甘正传/Forrest Gump'},
#  {'abstract': '最美的谎言。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p510861873.jpg',
#   'title': '美丽人生/La vita è bella'},
#  {'abstract': '最好的宫崎骏，最好的久石让。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1910830216.jpg',
#   'title': '千与千寻/千と千尋の神隠し'},
#  {'abstract': '拯救一个人，就是拯救整个世界。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p492406163.jpg',
#   'title': "辛德勒的名单/Schindler's List"},
#  {'abstract': '失去的才是永恒的。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p457760035.jpg',
#   'title': '泰坦尼克号/Titanic'},
#  {'abstract': '诺兰给了我们一场无法盗取的梦。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p513344864.jpg',
#   'title': '盗梦空间/Inception'},
#  {'abstract': '小瓦力，大人生。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p449665982.jpg',
#   'title': '机器人总动员/WALL·E'},
#  {'abstract': '每个人都要走一条自己坚定了的路，就算是粉身碎骨。',
#   'cover': 'https://img1.doubanio.com/view/movie_poster_cover/ipst/public/p511146957.jpg',
#   'title': "海上钢琴师/La leggenda del pianista sull'oceano"},
#  {'abstract': '英俊版憨豆，高情商版谢耳朵。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p579729551.jpg',
#   'title': '三傻大闹宝莱坞/3 Idiots'},
#  {'abstract': '永远都不能忘记你所爱的人。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p524964016.jpg',
#   'title': "忠犬八公的故事/Hachi: A Dog's Tale"},
#  {'abstract': '天籁一般的童声，是最接近上帝的存在。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1910824951.jpg',
#   'title': '放牛班的春天/Les choristes'},
#  {'abstract': '一生所爱。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p2455050536.jpg',
#   'title': '大话西游之大圣娶亲/西遊記大結局之仙履奇緣'},
#  {'abstract': '千万不要记恨你的对手，这样会让你失去理智。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1853232210.jpg',
#   'title': '教父/The Godfather'},
#  {'abstract': '人人心中都有个龙猫，童年就永远不会消失。',
#   'cover': 'https://img1.doubanio.com/view/movie_poster_cover/ipst/public/p1910829638.jpg',
#   'title': '龙猫/となりのトトロ'},
#  {'abstract': '如果再也不能见到你，祝你早安，午安，晚安。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p479682972.jpg',
#   'title': '楚门的世界/The Truman Show'},
#  {'abstract': 'Tomorrow is another day.',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1963126880.jpg',
#   'title': '乱世佳人/Gone with the Wind'},
#  {'abstract': '那些吻戏，那些青春，都在影院的黑暗里被泪水冲刷得无比清晰。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1910901025.jpg',
#   'title': '天堂电影院/Nuovo Cinema Paradiso'},
#  {'abstract': '平民励志片。',
#   'cover': 'https://img1.doubanio.com/view/movie_poster_cover/ipst/public/p1312700628.jpg',
#   'title': '当幸福来敲门/The Pursuit of Happyness'},
#  {'abstract': '满满温情的高雅喜剧。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1454261925.jpg',
#   'title': '触不可及/Intouchables'},
#  {'abstract': '邪恶与平庸蛰伏于同一个母体，在特定的时间互相对峙。',
#   'cover': 'https://img1.doubanio.com/view/movie_poster_cover/ipst/public/p1910926158.jpg',
#   'title': '搏击俱乐部/Fight Club'},
#  {'abstract': '1957年的理想主义。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p2173577632.jpg',
#   'title': '十二怒汉/12 Angry Men'},
#  {'abstract': '香港电影史上永不过时的杰作。',
#   'cover': 'https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p2233971046.jpg',
#   'title': '无间道/無間道'}]
```

