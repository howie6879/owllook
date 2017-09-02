#!/usr/bin/env python
import time
from talonspider import Item, TextField, AttrField
from pprint import pprint


class TestSpider(Item):
    title = TextField(css_select='.book-info>h1>em')
    author = TextField(css_select='a.writer')
    cover = AttrField(css_select='a#bookImg>img', attr='src')
    abstract = TextField(css_select='div.book-intro>p')
    tag = TextField(css_select='span.blue')
    latest_chapter = TextField(css_select='div.detail>p.cf>a')
    latest_chapter_time = TextField(css_select='div.detail>p.cf>em')

    def tal_title(self, title):
        # Clean your target value
        return title

    def tal_cover(self, cover):
        return 'http:' + cover

    def tal_tag(self, ele_tag):
        return '#'.join([i.text for i in ele_tag])

    def tal_latest_chapter_time(self, latest_chapter_time):
        return latest_chapter_time.replace('今天', str(time.strftime("%Y-%m-%d ", time.localtime())))


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


html = """

<!DOCTYPE html>
<html lang="zh-cmn-Hans" class="ua-mac ua-webkit">
<head>
    <title>豆瓣电影TOP250</title>
</head>
<body>
<ol class="grid_view">
        <li>
            <div class="item">
                <div class="pic">
                    <em class="">1</em>
                    <a href="https://movie.douban.com/subject/1292052/">
                        <img alt="肖申克的救赎" src="https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p480747492.webp" class="">
                    </a>
                </div>
                <div class="info">
                    <div class="hd">
                        <a href="https://movie.douban.com/subject/1292052/" class="">
                            <span class="title">肖申克的救赎</span>
                                    <span class="title">&nbsp;/&nbsp;The Shawshank Redemption</span>
                                <span class="other">&nbsp;/&nbsp;月黑高飞(港)  /  刺激1995(台)</span>
                        </a>


                            <span class="playable">[可播放]</span>
                    </div>
                    <div class="bd">
                        <p class="">
                            导演: 弗兰克·德拉邦特 Frank Darabont&nbsp;&nbsp;&nbsp;主演: 蒂姆·罗宾斯 Tim Robbins /...<br>
                            1994&nbsp;/&nbsp;美国&nbsp;/&nbsp;犯罪 剧情
                        </p>

                        
                        <div class="star">
                                <span class="rating5-t"></span>
                                <span class="rating_num" property="v:average">9.6</span>
                                <span property="v:best" content="10.0"></span>
                                <span>827737人评价</span>
                        </div>

                            <p class="quote">
                                <span class="inq">希望让人自由。</span>
                            </p>
                    </div>
                </div>
            </div>
        </li>
        <li>
            <div class="item">
                <div class="pic">
                    <em class="">2</em>
                    <a href="https://movie.douban.com/subject/1295644/">
                        <img alt="这个杀手不太冷" src="https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p511118051.webp" class="">
                    </a>
                </div>
                <div class="info">
                    <div class="hd">
                        <a href="https://movie.douban.com/subject/1295644/" class="">
                            <span class="title">这个杀手不太冷</span>
                                    <span class="title">&nbsp;/&nbsp;Léon</span>
                                <span class="other">&nbsp;/&nbsp;杀手莱昂  /  终极追杀令(台)</span>
                        </a>


                            <span class="playable">[可播放]</span>
                    </div>
                    <div class="bd">
                        <p class="">
                            导演: 吕克·贝松 Luc Besson&nbsp;&nbsp;&nbsp;主演: 让·雷诺 Jean Reno / 娜塔丽·波特曼 ...<br>
                            1994&nbsp;/&nbsp;法国&nbsp;/&nbsp;剧情 动作 犯罪
                        </p>

                        
                        <div class="star">
                                <span class="rating45-t"></span>
                                <span class="rating_num" property="v:average">9.4</span>
                                <span property="v:best" content="10.0"></span>
                                <span>794131人评价</span>
                        </div>

                            <p class="quote">
                                <span class="inq">怪蜀黍和小萝莉不得不说的故事。</span>
                            </p>
                    </div>
                </div>
            </div>
        </li>
        <li>
            <div class="item">
                <div class="pic">
                    <em class="">3</em>
                    <a href="https://movie.douban.com/subject/1291546/">
                        <img alt="霸王别姬" src="https://img3.doubanio.com/view/movie_poster_cover/ipst/public/p1910813120.webp" class="">
                    </a>
                </div>
                <div class="info">
                    <div class="hd">
                        <a href="https://movie.douban.com/subject/1291546/" class="">
                            <span class="title">霸王别姬</span>
                                <span class="other">&nbsp;/&nbsp;再见，我的妾  /  Farewell My Concubine</span>
                        </a>


                            <span class="playable">[可播放]</span>
                    </div>
                    <div class="bd">
                        <p class="">
                            导演: 陈凯歌 Kaige Chen&nbsp;&nbsp;&nbsp;主演: 张国荣 Leslie Cheung / 张丰毅 Fengyi Zha...<br>
                            1993&nbsp;/&nbsp;中国大陆 香港&nbsp;/&nbsp;剧情 爱情 同性
                        </p>

                        
                        <div class="star">
                                <span class="rating5-t"></span>
                                <span class="rating_num" property="v:average">9.5</span>
                                <span property="v:best" content="10.0"></span>
                                <span>591518人评价</span>
                        </div>

                            <p class="quote">
                                <span class="inq">风华绝代。</span>
                            </p>
                    </div>
                </div>
            </div>
        </li>
</body>
</html>
"""

if __name__ == '__main__':
    # 01
    item_data = TestSpider.get_item(url='http://book.qidian.com/info/1004608738')
    pprint(item_data)

    # 02
    # items_data = DoubanSpider.get_items(html=html)
    # result = []
    # for item in items_data:
    #     result.append({
    #         'title': item.title,
    #         'cover': item.cover,
    #         'abstract': item.abstract,
    #     })
    # pprint(result)

    # output01

    # {'abstract': '在破败中崛起，在寂灭中复苏。',
    #  'author': '辰东',
    #  'cover': 'http://qidian.qpic.cn/qdbimg/349573/1004608738/180',
    #  'latest_chapter': '求下月票啦，请投来吧',
    #  'latest_chapter_time': '2017-06-01 01:19更新',
    #  'spider_name': 'testspider',
    #  'tag': '连载#签约#VIP',
    #  'title': '圣墟'}

    # output02
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
