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
                username=self.MONGODB['USERNAME'],
                password=self.MONGODB['PASSWORD']) if self.MONGODB['USERNAME'] else '',
            host=self.MONGODB['HOST'] if self.MONGODB['HOST'] else 'localhost',
            port=self.MONGODB['PORT'] if self.MONGODB['PORT'] else 27017,
            database=db)
        return AsyncIOMotorClient(self.motor_uri)

    @property
    def db(self):
        if self._db is None:
            self._db = self.client(self.MONGODB['DATABASE'])[self.MONGODB['DATABASE']]

        return self._db
