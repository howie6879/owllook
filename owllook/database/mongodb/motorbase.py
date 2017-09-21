#!/usr/bin/env python
from motor.motor_asyncio import AsyncIOMotorClient
from owllook.utils.tools import singleton
from owllook.config import CONFIG


@singleton
class MotorBase:
    """
    更改mongodb连接方式 单例模式下支持多库操作
    About motor's doc: https://github.com/mongodb/motor
    """
    _db = {}
    _collection = {}
    MONGODB = CONFIG.MONGODB

    def __init__(self):
        self.motor_uri = ''

    def client(self, db):
        # motor
        self.motor_uri = 'mongodb://{account}{host}:{port}/{database}'.format(
            account='{username}:{password}@'.format(
                username=self.MONGODB['MONGO_USERNAME'],
                password=self.MONGODB['MONGO_PASSWORD']) if self.MONGODB['MONGO_USERNAME'] else '',
            host=self.MONGODB['MONGO_HOST'] if self.MONGODB['MONGO_HOST'] else 'localhost',
            port=self.MONGODB['MONGO_PORT'] if self.MONGODB['MONGO_PORT'] else 27017,
            database=db)
        return AsyncIOMotorClient(self.motor_uri)

    def get_db(self, db=MONGODB['DATABASE']):
        """
        Get a db instance
        :param db: database name
        :return: the motor db instance
        """
        if db not in self._db:
            self._db[db] = self.client(db)[db]

        return self._db[db]

    def get_collection(self, db_name, collection):
        """
        Get a collection instance
        :param db_name: database name
        :param collection: collection name
        :return: the motor collection instance
        """
        collection_key = db_name + collection
        if collection_key not in self._collection:
            self._collection[collection_key] = self.get_db(db_name)[collection]

        return self._collection[collection_key]

# class MotorBase:
#     """
#     use motor to connect mongodb
#     2017-09-21 deleted
#     """
#     _db = None
#     MONGODB = CONFIG.MONGODB
#
#     def client(self, db):
#         # motor
#         self.motor_uri = 'mongodb://{account}{host}:{port}/{database}'.format(
#             account='{username}:{password}@'.format(
#                 username=self.MONGODB['MONGO_USERNAME'],
#                 password=self.MONGODB['MONGO_PASSWORD']) if self.MONGODB['MONGO_USERNAME'] else '',
#             host=self.MONGODB['MONGO_HOST'] if self.MONGODB['MONGO_HOST'] else 'localhost',
#             port=self.MONGODB['MONGO_PORT'] if self.MONGODB['MONGO_PORT'] else 27017,
#             database=db)
#         return AsyncIOMotorClient(self.motor_uri)
#
#     @property
#     def db(self):
#         if self._db is None:
#             self._db = self.client(self.MONGODB['DATABASE'])[self.MONGODB['DATABASE']]
#
#         return self._db
