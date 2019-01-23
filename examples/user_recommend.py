#!/usr/bin/env python
import asyncio
import collections
import os
from operator import itemgetter

import uvloop

os.environ['MODE'] = 'DEV'

from pprint import pprint
from copy import deepcopy
from owllook.database.mongodb import MotorBase
from owllook.recommend.cosinesimilarity import CosineSimilarity
from owllook.fetcher.function import get_time


async def get_user_tag():
    motor_db = MotorBase().get_db()
    user_tag_cursor = motor_db.user_tag.find({}, {'data': 1, 'user': 1, '_id': 0})
    result = {}
    user_book_dict = {}

    async for document in user_tag_cursor:
        if document['data']:
            user_book_dict[document['user'].replace('.', '&#183;')] = document['data']
            result[document['user'].replace('.', '&#183;')] = document['data']['user_tag']

    for key, value in result.items():
        if not value:
            continue
        print("\nUser:", key)
        print("User tags:", set(value))
        print("User books:", user_book_dict[key]["user_novels"])
        result_copy = deepcopy(result)
        del result_copy[key]
        cos = CosineSimilarity(value, result_copy)
        vector = cos.create_vector()
        resultDic = cos.calculate(vector)
        print("相似用户:")
        pprint(resultDic[:10])
        # pprint(type(resultList[1]))
        booksDic = collections.defaultdict(float)
        for userBooks in resultDic:
            for simuser, simrate in userBooks.items():
                # print(simuser, simrate)
                for book in user_book_dict[simuser]["user_novels"]:
                    booksDic[book] += simrate
        # print(booksDic)
        # 推荐20本书，注意这里的推荐并没有去除用户收藏的书籍
        recommend = sorted(booksDic.items(), key=itemgetter(1), reverse=True)[0:20]
        print("书籍推荐：")
        pprint(recommend)
        recommend_novels = [book for book, simrate in recommend]
        await motor_db.user_recommend.update_one(
            {"user": key},
            {'$set': {'similar_user': resultDic, 'user_tag': result[key], 'recommend_novels': recommend_novels,
                      "updated_at": get_time()}}, upsert=True)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def get_user_tag_test():
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(get_user_tag())
    loop.run_until_complete(task)
    return task.result()


if __name__ == '__main__':
    get_user_tag_test()
