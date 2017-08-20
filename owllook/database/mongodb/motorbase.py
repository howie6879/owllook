#!/usr/bin/env python
from motor.motor_asyncio import AsyncIOMotorClient
from owllook.config import CONFIG


class MotorBase:
    """
    use motor to connect mongodb
    """
    _db = None
    MONGODB = CONFIG.MONGODB

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

    @property
    def db(self):
        if self._db is None:
            self._db = self.client(self.MONGODB['DATABASE'])[self.MONGODB['DATABASE']]

        return self._db
