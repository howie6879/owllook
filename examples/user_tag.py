#!/usr/bin/env python
import asyncio
import os
import pymongo
import uvloop

os.environ['MODE'] = 'PRO'

from pprint import pprint
from urllib.parse import parse_qs, urlparse

from owllook.database.mongodb import MotorBase
from owllook.fetcher.function import get_time

# mongo
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_USERNAME = ""
MONGODB_PASSWORD = ""
MONGODB_DB = "owllook"
MONGODB_COLLECTION = "all_novels_info"


class Novels(object):
    def __init__(self):
        _mongo_uri = 'mongodb://{account}{host}:{port}/{database}'.format(
            account='{username}:{password}@'.format(
                username=MONGODB_USERNAME,
                password=MONGODB_PASSWORD) if MONGODB_USERNAME else '',
            host='localhost',
            port=27017,
            database=MONGODB_DB)
        connection = pymongo.MongoClient(_mongo_uri)
        db = connection[MONGODB_DB]
        self.collection = db[MONGODB_COLLECTION]
        self.result_dict = dict()

    def search_name(self, name):
        if name in self.result_dict:
            return self.result_dict[name] if self.result_dict[name] else False
        result = self.collection.find_one({'novel_name': name})
        if not result:
            self.result_dict[name] = False
            return False
        self.result_dict[name] = {'author': result['author'], 'novels_type': result['novels_type'].split('#')}
        return self.result_dict[name]


async def get_tag():
    motor_db = MotorBase().get_db()
    novels = Novels()
    # 获取所有书架链接游标
    books_url_cursor = motor_db.user_message.find({}, {'books_url.book_url': 1, 'user': 1, '_id': 0})
    async for document in books_url_cursor:
        if document:
            books_url = document.get('books_url', None)
            user = document['user']
            if books_url:
                all_user = {user + '_novels': [], user + '_tag': [], user + '_author': []}
                for book_url in books_url:
                    chapter_url = book_url['book_url']
                    novels_name = parse_qs(urlparse(chapter_url).query).get('novels_name', '')[0]
                    all_user[user + '_novels'].append(novels_name)
                    novels_info = novels.search_name(novels_name)
                    if novels_info:
                        all_user[user + '_author'].append(novels_info['author'])
                        all_user[user + '_tag'].extend(novels_info['novels_type'])
                data = {
                    'user_novels': all_user[user + '_novels'],
                    'user_tag': all_user[user + '_tag'],
                    'user_author': all_user[user + '_author'],
                }
                await motor_db.user_tag.update_one(
                    {"user": user},
                    {'$set': {'data': data, "updated_at": get_time()}}, upsert=True)
                pprint(data)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def tag_test():
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(get_tag())
    loop.run_until_complete(task)
    return task.result()


if __name__ == '__main__':
    tag_test()
