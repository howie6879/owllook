#!/usr/bin/env python
from motor.motor_asyncio import AsyncIOMotorClient
from owllook.config import MONGODB


class MotorBase:
    """
    use motor to connect mongodb
    """
    _db = None

    def client(self, db):
        # motor
        self.motor_uri = 'mongodb://{account}{host}:{port}/{database}'.format(
            account='{username}:{password}@'.format(username=MONGODB['USERNAME'],
                                                    password=MONGODB['PASSWORD']) if MONGODB['USERNAME'] else '',
            host=MONGODB['HOST'] if MONGODB['HOST'] else 'localhost',
            port=MONGODB['PORT'] if MONGODB['PORT'] else 27017,
            database=db)
        return AsyncIOMotorClient(self.motor_uri)

    @property
    def db(self):
        if self._db is None:
            self._db = self.client(MONGODB['DATABASE'])[MONGODB['DATABASE']]

        return self._db
